
import Foundation

final class NetworkManager {
    
    var films: [Film] = []
    private let domainUrlString = "https://swapi.co/api/"
    
    func fetchFilms(completionHandler: @escaping ([Film]) -> Void) {
        let url = URL(string: domainUrlString + "films/")!
        
        let task = URLSession.shared.dataTask(with: url, completionHandler: { (data, response, error) in
            if let error = error {
                print("Error with fetching films: \(error)")
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse,
                (200...299).contains(httpResponse.statusCode) else {
                    print("Error with the response, unexpected status code: \(String(describing: response))")
                    return
            }
            
            if let data = data,
                let filmSummary = try? JSONDecoder().decode(FilmSummary.self, from: data) {
                completionHandler(filmSummary.results ?? [])
            }
        })
        task.resume()
    }
    
    
    func fetchSound(completionHandler: @escaping ([Sound]) -> Void) {
        let jetsonurl = URL(string: "http://192.168.3.100/data.txt")!
        
        let task = URLSession.shared.dataTask(with: jetsonurl, completionHandler: { (data, response, error) in
            if let error = error {
                print("Error with fetching films: \(error)")
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse,
                (200...299).contains(httpResponse.statusCode) else {
                    print("Error with the response, unexpected status code: \(String(describing: response))")
                    return
            }
            
            if let data = data,
                let soundSummary = try? JSONDecoder().decode(SoundSummary.self, from: data) {
                completionHandler(soundSummary.data ?? [])
            }
        })
        task.resume()
    }
    
    private func fetchFilm(withID id:Int, completionHandler: @escaping (Film) -> Void) {
        let url = URL(string: domainUrlString + "films/\(id)")!
        
        let task = URLSession.shared.dataTask(with: url) { (data, response, error) in
            if let error = error {
                print("Error returning film id \(id): \(error)")
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse,
                (200...299).contains(httpResponse.statusCode) else {
                    print("Unexpected response status code: \(String(describing: response))")
                    return
            }
            
            if let data = data,
                let film = try? JSONDecoder().decode(Film.self, from: data) {
                completionHandler(film)
            }
        }
        task.resume()
    }
}
