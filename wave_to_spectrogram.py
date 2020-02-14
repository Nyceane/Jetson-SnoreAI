import tensorflow as tf
# FIXME: audio_ops.decode_wav is deprecated, use tensorflow_io.IOTensor.from_audio
from tensorflow.contrib.framework.python.ops import audio_ops

# Enable eager execution for a more interactive frontend.
# If using the default graph mode, you'll probably need to run in a session.
tf.enable_eager_execution()

@tf.function
def audio_to_spectrogram(
        audio_contents,
        width,
        height,
        channels=1,
        window_size=1024,
        stride=64,
        brightness=100.):
    """Decode and build a spectrogram using a wav string tensor.

    Args:
      audio_contents: String tensor of the wav audio contents.
      width: Spectrogram width.
      height: Spectrogram height.
      channels: Audio channel count.
      window_size: Size of the spectrogram window.
      stride: Size of the spectrogram stride.
      brightness: Brightness of the spectrogram.

    Returns:
      0-D string Tensor with the image contents.
    """
    # Decode the wav mono into a 2D tensor with time in dimension 0
    # and channel along dimension 1
    waveform = audio_ops.decode_wav(audio_contents, desired_channels=channels)
	
    # Compute the spectrogram
    # FIXME: Seems like this is deprecated in tensorflow 2.0 and
    # the operation only works on CPU. Change this to tf.signal.stft 
    # and  friends to take advantage of GPU kernels.
    spectrogram = audio_ops.audio_spectrogram(
        	waveform.audio,
        	window_size=window_size,
        	stride=stride)

    # Adjust brightness
    brightness = tf.constant(brightness)

    # Normalize pixels
    mul = tf.multiply(spectrogram, brightness)
    min_const = tf.constant(255.)
    minimum = tf.minimum(mul, min_const)

    # Expand dims so we get the proper shape
    expand_dims = tf.expand_dims(minimum, -1)

    # Resize the spectrogram to input size of the model
    resize = tf.image.resize(expand_dims, [width, height])

    # Remove the trailing dimension
    squeeze = tf.squeeze(resize, 0)

    # Tensorflow spectrogram has time along y axis and frequencies along x axis
    # so we fix that
    flip_left_right = tf.image.flip_left_right(squeeze)
    transposed = tf.image.transpose(flip_left_right)

    # Cast to uint8 and encode as png
    cast = tf.cast(transposed, tf.uint8)

    # Encode tensor as a png image
    return tf.image.encode_png(cast)

if __name__ == '__main__':
    input_file = tf.constant('record.wav')
    output_file = tf.constant('spectrogram.png')

    # Generage the spectrogram
    audio = tf.io.read_file(input_file)
    image = audio_to_spectrogram(audio, 224, 224)

    # Write the png encoded image to a file
    tf.io.write_file(output_file, image)
