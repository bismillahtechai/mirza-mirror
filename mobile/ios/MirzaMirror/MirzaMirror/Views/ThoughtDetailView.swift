import SwiftUI

struct ThoughtDetailView: View {
    let thought: Thought
    @EnvironmentObject var thoughtStore: ThoughtStore
    @State private var showingActionSheet = false
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                // Content section
                VStack(alignment: .leading, spacing: 8) {
                    Text(thought.content)
                        .font(.body)
                        .padding()
                        .background(Color(.systemGray6))
                        .cornerRadius(8)
                    
                    HStack {
                        Image(systemName: "calendar")
                            .foregroundColor(.gray)
                        Text(formattedDate(thought.createdAt))
                            .font(.caption)
                            .foregroundColor(.gray)
                        
                        Spacer()
                        
                        Image(systemName: "tag")
                            .foregroundColor(.gray)
                        Text("\(thought.tags.count) tags")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                }
                .padding(.horizontal)
                
                Divider()
                
                // Tags section
                if !thought.tags.isEmpty {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Tags")
                            .font(.headline)
                        
                        FlowLayout(spacing: 8) {
                            ForEach(thought.tags) { tag in
                                Text(tag.name)
                                    .font(.caption)
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 4)
                                    .background(Color.blue.opacity(0.2))
                                    .cornerRadius(8)
                            }
                        }
                    }
                    .padding(.horizontal)
                    
                    Divider()
                }
                
                // Summary section
                if let summary = thought.summary, !summary.isEmpty {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Summary")
                            .font(.headline)
                        
                        Text(summary)
                            .font(.body)
                            .padding()
                            .background(Color(.systemGray6))
                            .cornerRadius(8)
                    }
                    .padding(.horizontal)
                    
                    Divider()
                }
                
                // Actions section
                if !thought.actions.isEmpty {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Actions")
                            .font(.headline)
                        
                        ForEach(thought.actions) { action in
                            HStack(alignment: .top) {
                                Image(systemName: action.completed ? "checkmark.circle.fill" : "circle")
                                    .foregroundColor(action.completed ? .green : .gray)
                                
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(action.content)
                                        .font(.body)
                                        .strikethrough(action.completed)
                                    
                                    HStack {
                                        Text(priorityText(action.priority))
                                            .font(.caption)
                                            .foregroundColor(priorityColor(action.priority))
                                            .padding(.horizontal, 8)
                                            .padding(.vertical, 2)
                                            .background(priorityColor(action.priority).opacity(0.2))
                                            .cornerRadius(4)
                                        
                                        if let dueDate = action.dueDate, !dueDate.isEmpty {
                                            Text(dueDate)
                                                .font(.caption)
                                                .foregroundColor(.gray)
                                        }
                                    }
                                }
                                
                                Spacer()
                            }
                            .padding()
                            .background(Color(.systemGray6))
                            .cornerRadius(8)
                        }
                    }
                    .padding(.horizontal)
                    
                    Divider()
                }
                
                // Related thoughts section
                if !thought.links.isEmpty {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Related Thoughts")
                            .font(.headline)
                        
                        ForEach(thought.links) { link in
                            HStack {
                                Image(systemName: relationshipIcon(link.relationship))
                                    .foregroundColor(.blue)
                                
                                Text(link.relationship.capitalized)
                                    .font(.caption)
                                    .foregroundColor(.gray)
                                
                                Spacer()
                                
                                Text("Strength: \(Int(link.strength * 100))%")
                                    .font(.caption)
                                    .foregroundColor(.gray)
                            }
                            .padding()
                            .background(Color(.systemGray6))
                            .cornerRadius(8)
                        }
                    }
                    .padding(.horizontal)
                }
                
                // Audio or document attachments
                if thought.audioFile != nil || thought.documentFile != nil {
                    Divider()
                    
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Attachments")
                            .font(.headline)
                        
                        if let audioFile = thought.audioFile {
                            HStack {
                                Image(systemName: "waveform")
                                    .foregroundColor(.blue)
                                
                                Text("Audio Recording")
                                    .font(.body)
                                
                                Spacer()
                                
                                Button(action: {
                                    // Play audio logic would go here
                                }) {
                                    Image(systemName: "play.circle")
                                        .font(.title2)
                                }
                            }
                            .padding()
                            .background(Color(.systemGray6))
                            .cornerRadius(8)
                        }
                        
                        if let documentFile = thought.documentFile {
                            HStack {
                                Image(systemName: "doc")
                                    .foregroundColor(.blue)
                                
                                Text(documentFile.components(separatedBy: "/").last ?? "Document")
                                    .font(.body)
                                
                                Spacer()
                                
                                Button(action: {
                                    // View document logic would go here
                                }) {
                                    Image(systemName: "eye")
                                        .font(.title2)
                                }
                            }
                            .padding()
                            .background(Color(.systemGray6))
                            .cornerRadius(8)
                        }
                    }
                    .padding(.horizontal)
                }
            }
            .padding(.vertical)
        }
        .navigationTitle("Thought Details")
        .navigationBarItems(trailing: Button(action: {
            showingActionSheet = true
        }) {
            Image(systemName: "ellipsis")
        })
        .actionSheet(isPresented: $showingActionSheet) {
            ActionSheet(
                title: Text("Options"),
                buttons: [
                    .default(Text("Share")) {
                        // Share logic would go here
                    },
                    .default(Text("Edit")) {
                        // Edit logic would go here
                    },
                    .destructive(Text("Delete")) {
                        // Delete logic would go here
                    },
                    .cancel()
                ]
            )
        }
    }
    
    private func formattedDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
    
    private func priorityText(_ priority: String) -> String {
        switch priority.lowercased() {
        case "high":
            return "High Priority"
        case "medium":
            return "Medium Priority"
        case "low":
            return "Low Priority"
        default:
            return priority.capitalized
        }
    }
    
    private func priorityColor(_ priority: String) -> Color {
        switch priority.lowercased() {
        case "high":
            return .red
        case "medium":
            return .orange
        case "low":
            return .blue
        default:
            return .gray
        }
    }
    
    private func relationshipIcon(_ relationship: String) -> String {
        switch relationship.lowercased() {
        case "similar":
            return "equal.circle"
        case "continuation":
            return "arrow.right.circle"
        case "contradiction":
            return "xmark.circle"
        case "inspiration":
            return "lightbulb.circle"
        default:
            return "link.circle"
        }
    }
}

// FlowLayout for tags
struct FlowLayout: Layout {
    var spacing: CGFloat = 8
    
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout Void) -> CGSize {
        let width = proposal.width ?? .infinity
        var height: CGFloat = 0
        var x: CGFloat = 0
        var y: CGFloat = 0
        var maxHeight: CGFloat = 0
        
        for view in subviews {
            let size = view.sizeThatFits(.unspecified)
            if x + size.width > width {
                x = 0
                y += maxHeight + spacing
                maxHeight = 0
            }
            
            maxHeight = max(maxHeight, size.height)
            x += size.width + spacing
        }
        
        height = y + maxHeight
        
        return CGSize(width: width, height: height)
    }
    
    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout Void) {
        let width = bounds.width
        var x = bounds.minX
        var y = bounds.minY
        var maxHeight: CGFloat = 0
        
        for view in subviews {
            let size = view.sizeThatFits(.unspecified)
            if x + size.width > width + bounds.minX {
                x = bounds.minX
                y += maxHeight + spacing
                maxHeight = 0
            }
            
            view.place(at: CGPoint(x: x, y: y), proposal: ProposedViewSize(size))
            maxHeight = max(maxHeight, size.height)
            x += size.width + spacing
        }
    }
}

struct ThoughtDetailView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            ThoughtDetailView(thought: Thought(
                id: "1",
                content: "This is a sample thought for preview purposes. It demonstrates how the detail view will look with actual content.",
                source: "ios_app",
                createdAt: Date(),
                updatedAt: Date(),
                audioFile: nil,
                documentFile: nil,
                summary: "This is a summary of the thought that was automatically generated.",
                tags: [
                    Tag(id: "1", name: "important", type: "auto", confidence: 0.9),
                    Tag(id: "2", name: "work", type: "auto", confidence: 0.8),
                    Tag(id: "3", name: "idea", type: "auto", confidence: 0.7)
                ],
                links: [
                    Link(id: "1", sourceThoughtId: "1", targetThoughtId: "2", relationship: "similar", strength: 0.8)
                ],
                actions: [
                    Action(id: "1", content: "Follow up on this idea", priority: "high", dueDate: "2023-04-15", completed: false),
                    Action(id: "2", content: "Share with team", priority: "medium", dueDate: nil, completed: true)
                ]
            ))
            .environmentObject(ThoughtStore())
        }
    }
}
