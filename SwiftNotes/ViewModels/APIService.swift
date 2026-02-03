import Foundation

class APIService: ObservableObject {
    static let shared = APIService()
    
    // IMPORTANT: On Simulator, use localhost. On Device, use Mac's LAN IP (e.g. 192.168.x.x)
    private let baseURL = "http://localhost:8000/api"
    
    func fetchSessions() async throws -> [VideoSession] {
        guard let url = URL(string: "\(baseURL)/knowledge") else {
            throw URLError(.badURL)
        }
        
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode([VideoSession].self, from: data)
    }
    
    func fetchKnowledge(for id: String) async throws -> KnowledgeGraph {
        guard let url = URL(string: "\(baseURL)/knowledge/\(id)") else {
            throw URLError(.badURL)
        }
        
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(KnowledgeGraph.self, from: data)
    }
}
