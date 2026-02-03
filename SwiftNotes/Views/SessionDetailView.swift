import SwiftUI
import AVKit

struct SessionDetailView: View {
    let session: VideoSession
    @State private var knowledge: KnowledgeGraph?
    @State private var isLoading = true
    
    // For Video Player
    @State private var player: AVPlayer?
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                
                // 1. Video Player Area
                ZStack {
                    if let player = player {
                        VideoPlayer(player: player)
                            .aspectRatio(16/9, contentMode: .fit)
                            .cornerRadius(12)
                    } else {
                        Rectangle()
                            .fill(Color.black.opacity(0.8))
                            .aspectRatio(16/9, contentMode: .fit)
                            .overlay(
                                Image(systemName: "play.circle.fill")
                                    .font(.system(size: 50))
                                    .foregroundStyle(.white)
                            )
                            .cornerRadius(12)
                    }
                }
                
                // 2. Knowledge Sections
                if isLoading {
                    ProgressView("Loading Brain...")
                        .frame(maxWidth: .infinity)
                        .padding(.top, 40)
                } else if let k = knowledge {
                    
                    // Theory Section
                    KnowledgeSection(title: "Theory", icon: "book.fill", color: .blue) {
                        ForEach(k.theory) { item in
                            VStack(alignment: .leading, spacing: 8) {
                                Text(item.title).font(.headline)
                                Text(item.explanation).font(.body).foregroundStyle(.secondary)
                            }
                            .padding()
                            .background(Color(.secondarySystemBackground))
                            .cornerRadius(10)
                        }
                    }
                    
                    // Formulas Section
                    if !k.formulas.isEmpty {
                        KnowledgeSection(title: "Formulas", icon: "function", color: .purple) {
                            ForEach(k.formulas) { item in
                                VStack(alignment: .leading, spacing: 8) {
                                    Text(item.name).font(.headline)
                                    Text(item.equation)
                                        .font(.system(.title3, design: .monospaced))
                                        .foregroundStyle(.primary)
                                        .padding(.vertical, 4)
                                    Text("Usage: \(item.usage)").font(.caption)
                                }
                                .padding()
                                .background(Color.purple.opacity(0.1))
                                .cornerRadius(10)
                            }
                        }
                    }
                }
            }
            .padding()
        }
        .navigationTitle(session.title)
        .onAppear {
            loadData()
            setupVideo()
        }
    }
    
    func loadData() {
        Task {
            do {
                knowledge = try await APIService.shared.fetchKnowledge(for: session.id)
                isLoading = false
            } catch {
                print("Failed to load knowledge: \(error)")
                isLoading = false
            }
        }
    }
    
    func setupVideo() {
        // Pointing to local backend file serve
        // Ensure backend mounts static files correctly!
        if let url = URL(string: "http://localhost:8000/files/videos/\(session.id).mp4") {
            player = AVPlayer(url: url)
        }
    }
}

// Helper View for Sections
struct KnowledgeSection<Content: View>: View {
    let title: String
    let icon: String
    let color: Color
    @ViewBuilder let content: Content
    
    var body: some View {
        VStack(alignment: .leading) {
            HStack {
                Image(systemName: icon)
                    .foregroundStyle(color)
                Text(title)
                    .font(.title2)
                    .bold()
            }
            .padding(.bottom, 8)
            
            content
        }
    }
}
