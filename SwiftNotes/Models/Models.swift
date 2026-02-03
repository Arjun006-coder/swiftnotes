import Foundation

// MARK: - API Response Models

struct VideoSession: Identifiable, Codable, Hashable {
    let video_id: String
    let title: String
    let topic_count: Int
    let difficulty: String
    
    // For List compatibility
    var id: String { video_id }
}

struct KnowledgeGraph: Codable {
    let video_id: String
    let theory: [TheoryItem]
    let formulas: [FormulaItem]
    let examples: [ExampleItem]
}

struct TheoryItem: Identifiable, Codable {
    let title: String
    let explanation: String
    var id: String { title }
}

struct FormulaItem: Identifiable, Codable {
    let name: String
    let equation: String
    let usage: String
    var id: String { name }
}

struct ExampleItem: Identifiable, Codable {
    let problem: String
    let solution: String
    var id: String { problem }
}
