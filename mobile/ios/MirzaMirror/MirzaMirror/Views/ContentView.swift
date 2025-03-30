import SwiftUI
import AVFoundation

struct ContentView: View {
    @EnvironmentObject var thoughtStore: ThoughtStore
    @State private var searchText = ""
    @State private var showingAddThought = false
    @State private var showingVoiceCapture = false
    @State private var showingDocumentPicker = false
    @State private var isRecording = false
    @State private var audioRecorder: AVAudioRecorder?
    @State private var recordingURL: URL?
    
    var body: some View {
        NavigationView {
            VStack {
                // Search bar
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundColor(.gray)
                    TextField("Search thoughts...", text: $searchText)
                        .onSubmit {
                            if !searchText.isEmpty {
                                thoughtStore.searchThoughts(query: searchText)
                            } else {
                                thoughtStore.fetchThoughts()
                            }
                        }
                    if !searchText.isEmpty {
                        Button(action: {
                            searchText = ""
                            thoughtStore.fetchThoughts()
                        }) {
                            Image(systemName: "xmark.circle.fill")
                                .foregroundColor(.gray)
                        }
                    }
                }
                .padding(8)
                .background(Color(.systemGray6))
                .cornerRadius(10)
                .padding(.horizontal)
                
                // Thoughts list
                if thoughtStore.isLoading {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle())
                        .scaleEffect(1.5)
                        .padding()
                } else if let error = thoughtStore.error {
                    VStack {
                        Image(systemName: "exclamationmark.triangle")
                            .font(.largeTitle)
                            .foregroundColor(.red)
                        Text(error)
                            .multilineTextAlignment(.center)
                            .padding()
                        Button("Try Again") {
                            thoughtStore.fetchThoughts()
                        }
                        .buttonStyle(.bordered)
                    }
                    .padding()
                } else if thoughtStore.thoughts.isEmpty {
                    VStack {
                        Image(systemName: "doc.text")
                            .font(.largeTitle)
                            .foregroundColor(.gray)
                        Text("No thoughts found")
                            .foregroundColor(.gray)
                            .padding()
                        Button("Add Your First Thought") {
                            showingAddThought = true
                        }
                        .buttonStyle(.bordered)
                    }
                    .padding()
                } else {
                    List {
                        ForEach(thoughtStore.thoughts) { thought in
                            NavigationLink(destination: ThoughtDetailView(thought: thought)) {
                                ThoughtRow(thought: thought)
                            }
                        }
                    }
                    .listStyle(InsetGroupedListStyle())
                    .refreshable {
                        thoughtStore.fetchThoughts()
                    }
                }
            }
            .navigationTitle("Mirza Mirror")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Menu {
                        Button(action: {
                            showingAddThought = true
                        }) {
                            Label("Text Thought", systemImage: "text.bubble")
                        }
                        
                        Button(action: {
                            showingVoiceCapture = true
                        }) {
                            Label("Voice Thought", systemImage: "mic")
                        }
                        
                        Button(action: {
                            showingDocumentPicker = true
                        }) {
                            Label("Document", systemImage: "doc")
                        }
                    } label: {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingAddThought) {
                AddThoughtView()
            }
            .sheet(isPresented: $showingVoiceCapture) {
                VoiceCaptureView()
            }
            .sheet(isPresented: $showingDocumentPicker) {
                DocumentPickerView()
            }
            .onAppear {
                thoughtStore.fetchThoughts()
            }
        }
    }
}

struct ThoughtRow: View {
    let thought: Thought
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(thought.content)
                .lineLimit(2)
                .font(.body)
            
            HStack {
                Text(formattedDate(thought.createdAt))
                    .font(.caption)
                    .foregroundColor(.gray)
                
                Spacer()
                
                ForEach(thought.tags.prefix(3)) { tag in
                    Text(tag.name)
                        .font(.caption)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Color.blue.opacity(0.2))
                        .cornerRadius(8)
                }
            }
        }
        .padding(.vertical, 4)
    }
    
    private func formattedDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .environmentObject(ThoughtStore())
            .environmentObject(APIService())
    }
}
