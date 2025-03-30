import Foundation
import Combine

// MARK: - Thought Model
struct Thought: Identifiable, Codable {
    var id: String
    var content: String
    var source: String
    var createdAt: Date
    var updatedAt: Date
    var audioFile: String?
    var documentFile: String?
    var summary: String?
    var tags: [Tag]
    var links: [Link]
    var actions: [Action]
    
    enum CodingKeys: String, CodingKey {
        case id, content, source
        case createdAt = "created_at"
        case updatedAt = "updated_at"
        case audioFile = "audio_file"
        case documentFile = "document_file"
        case summary, tags, links, actions
    }
}

// MARK: - Tag Model
struct Tag: Identifiable, Codable {
    var id: String
    var name: String
    var type: String
    var confidence: Float?
    
    enum CodingKeys: String, CodingKey {
        case id, name, type, confidence
    }
}

// MARK: - Link Model
struct Link: Identifiable, Codable {
    var id: String
    var sourceThoughtId: String
    var targetThoughtId: String
    var relationship: String
    var strength: Float
    
    enum CodingKeys: String, CodingKey {
        case id
        case sourceThoughtId = "source_thought_id"
        case targetThoughtId = "target_thought_id"
        case relationship, strength
    }
}

// MARK: - Action Model
struct Action: Identifiable, Codable {
    var id: String
    var content: String
    var priority: String
    var dueDate: String?
    var completed: Bool
    
    enum CodingKeys: String, CodingKey {
        case id, content, priority
        case dueDate = "due_date"
        case completed
    }
}

// MARK: - Document Model
struct Document: Identifiable, Codable {
    var id: String
    var filePath: String
    var content: String?
    var contentType: String
    var createdAt: Date
    var updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case filePath = "file_path"
        case content
        case contentType = "content_type"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

// MARK: - ThoughtStore
class ThoughtStore: ObservableObject {
    @Published var thoughts: [Thought] = []
    @Published var isLoading: Bool = false
    @Published var error: String? = nil
    
    private var cancellables = Set<AnyCancellable>()
    private let apiService = APIService()
    
    func fetchThoughts() {
        isLoading = true
        error = nil
        
        apiService.fetchThoughts()
            .receive(on: DispatchQueue.main)
            .sink(receiveCompletion: { [weak self] completion in
                self?.isLoading = false
                if case .failure(let error) = completion {
                    self?.error = error.localizedDescription
                }
            }, receiveValue: { [weak self] thoughts in
                self?.thoughts = thoughts
            })
            .store(in: &cancellables)
    }
    
    func addThought(content: String, source: String = "ios_app") {
        isLoading = true
        error = nil
        
        apiService.addThought(content: content, source: source)
            .receive(on: DispatchQueue.main)
            .sink(receiveCompletion: { [weak self] completion in
                self?.isLoading = false
                if case .failure(let error) = completion {
                    self?.error = error.localizedDescription
                }
            }, receiveValue: { [weak self] thought in
                self?.thoughts.append(thought)
            })
            .store(in: &cancellables)
    }
    
    func searchThoughts(query: String) {
        isLoading = true
        error = nil
        
        apiService.searchThoughts(query: query)
            .receive(on: DispatchQueue.main)
            .sink(receiveCompletion: { [weak self] completion in
                self?.isLoading = false
                if case .failure(let error) = completion {
                    self?.error = error.localizedDescription
                }
            }, receiveValue: { [weak self] thoughts in
                self?.thoughts = thoughts
            })
            .store(in: &cancellables)
    }
}
