import Foundation
import Combine

enum APIError: Error {
    case invalidURL
    case networkError(Error)
    case decodingError(Error)
    case serverError(Int)
    case unknown
}

class APIService: ObservableObject {
    private let baseURL = "https://mirza-mirror-api.onrender.com" // Production URL on Render
    private var cancellables = Set<AnyCancellable>()
    
    // MARK: - Authentication
    @Published var isAuthenticated = false
    
    // MARK: - Thoughts API
    func fetchThoughts() -> AnyPublisher<[Thought], Error> {
        guard let url = URL(string: "\(baseURL)/api/thoughts") else {
            return Fail(error: APIError.invalidURL).eraseToAnyPublisher()
        }
        
        return URLSession.shared.dataTaskPublisher(for: url)
            .map(\.data)
            .decode(type: [Thought].self, decoder: JSONDecoder())
            .mapError { error -> Error in
                if let urlError = error as? URLError {
                    return APIError.networkError(urlError)
                } else if let decodingError = error as? DecodingError {
                    return APIError.decodingError(decodingError)
                } else {
                    return APIError.unknown
                }
            }
            .eraseToAnyPublisher()
    }
    
    func addThought(content: String, source: String) -> AnyPublisher<Thought, Error> {
        guard let url = URL(string: "\(baseURL)/api/capture/text") else {
            return Fail(error: APIError.invalidURL).eraseToAnyPublisher()
        }
        
        let parameters = ["content": content, "source": source]
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters)
        } catch {
            return Fail(error: error).eraseToAnyPublisher()
        }
        
        return URLSession.shared.dataTaskPublisher(for: request)
            .map(\.data)
            .decode(type: Thought.self, decoder: JSONDecoder())
            .mapError { error -> Error in
                if let urlError = error as? URLError {
                    return APIError.networkError(urlError)
                } else if let decodingError = error as? DecodingError {
                    return APIError.decodingError(decodingError)
                } else {
                    return APIError.unknown
                }
            }
            .eraseToAnyPublisher()
    }
    
    func searchThoughts(query: String) -> AnyPublisher<[Thought], Error> {
        guard var urlComponents = URLComponents(string: "\(baseURL)/api/thoughts/search") else {
            return Fail(error: APIError.invalidURL).eraseToAnyPublisher()
        }
        
        urlComponents.queryItems = [URLQueryItem(name: "query", value: query)]
        
        guard let url = urlComponents.url else {
            return Fail(error: APIError.invalidURL).eraseToAnyPublisher()
        }
        
        return URLSession.shared.dataTaskPublisher(for: url)
            .map(\.data)
            .decode(type: [Thought].self, decoder: JSONDecoder())
            .mapError { error -> Error in
                if let urlError = error as? URLError {
                    return APIError.networkError(urlError)
                } else if let decodingError = error as? DecodingError {
                    return APIError.decodingError(decodingError)
                } else {
                    return APIError.unknown
                }
            }
            .eraseToAnyPublisher()
    }
    
    // MARK: - Voice Capture
    func uploadVoiceRecording(audioData: Data) -> AnyPublisher<Thought, Error> {
        guard let url = URL(string: "\(baseURL)/api/capture/voice") else {
            return Fail(error: APIError.invalidURL).eraseToAnyPublisher()
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("audio/m4a", forHTTPHeaderField: "Content-Type")
        request.httpBody = audioData
        
        return URLSession.shared.dataTaskPublisher(for: request)
            .map(\.data)
            .decode(type: Thought.self, decoder: JSONDecoder())
            .mapError { error -> Error in
                if let urlError = error as? URLError {
                    return APIError.networkError(urlError)
                } else if let decodingError = error as? DecodingError {
                    return APIError.decodingError(decodingError)
                } else {
                    return APIError.unknown
                }
            }
            .eraseToAnyPublisher()
    }
    
    // MARK: - Document Upload
    func uploadDocument(documentData: Data, filename: String, contentType: String) -> AnyPublisher<Document, Error> {
        guard let url = URL(string: "\(baseURL)/api/documents") else {
            return Fail(error: APIError.invalidURL).eraseToAnyPublisher()
        }
        
        // Create multipart form data
        let boundary = "Boundary-\(UUID().uuidString)"
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        
        // Add the file data
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(filename)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: \(contentType)\r\n\r\n".data(using: .utf8)!)
        body.append(documentData)
        body.append("\r\n".data(using: .utf8)!)
        
        // Add content type
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"content_type\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(contentType)\r\n".data(using: .utf8)!)
        
        // Close the boundary
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        return URLSession.shared.dataTaskPublisher(for: request)
            .map(\.data)
            .decode(type: Document.self, decoder: JSONDecoder())
            .mapError { error -> Error in
                if let urlError = error as? URLError {
                    return APIError.networkError(urlError)
                } else if let decodingError = error as? DecodingError {
                    return APIError.decodingError(decodingError)
                } else {
                    return APIError.unknown
                }
            }
            .eraseToAnyPublisher()
    }
}
