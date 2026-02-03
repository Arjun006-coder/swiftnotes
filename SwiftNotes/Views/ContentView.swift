import SwiftUI

struct ContentView: View {
    @State private var sessions: [VideoSession] = []
    @State private var selectedSession: VideoSession?
    @State private var searchText = ""
    
    var filteredSessions: [VideoSession] {
        if searchText.isEmpty { return sessions }
        return sessions.filter { $0.title.localizedCaseInsensitiveContains(searchText) }
    }
    
    var body: some View {
        NavigationSplitView {
            List(filteredSessions, selection: $selectedSession) { session in
                NavigationLink(value: session) {
                    VStack(alignment: .leading) {
                        Text(session.title)
                            .font(.headline)
                        HStack {
                            Text(session.difficulty)
                                .font(.caption)
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(Color.gray.opacity(0.2))
                                .cornerRadius(4)
                            
                            Spacer()
                            Text("\(session.topic_count) topics")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                    .padding(.vertical, 4)
                }
            }
            .navigationTitle("Swift Notes 🍎")
            .searchable(text: $searchText, placement: .sidebar)
            .refreshable {
                await loadSessions()
            }
            .task {
                await loadSessions()
            }
        } detail: {
            if let session = selectedSession {
                SessionDetailView(session: session)
            } else {
                ContentUnavailableView(
                    "Select a Note",
                    systemImage: "note.text",
                    description: Text("Choose a session from the sidebar to start studying.")
                )
            }
        }
    }
    
    func loadSessions() async {
        do {
            sessions = try await APIService.shared.fetchSessions()
        } catch {
            print("Error loading sessions: \(error)")
        }
    }
}
