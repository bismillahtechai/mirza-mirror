import SwiftUI

struct AddThoughtView: View {
    @Environment(\.presentationMode) var presentationMode
    @EnvironmentObject var thoughtStore: ThoughtStore
    @State private var thoughtText = ""
    @State private var isSubmitting = false
    
    var body: some View {
        NavigationView {
            VStack {
                TextEditor(text: $thoughtText)
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(8)
                    .padding()
                    .frame(maxHeight: .infinity)
                
                if isSubmitting {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle())
                        .padding()
                }
            }
            .navigationTitle("New Thought")
            .navigationBarItems(
                leading: Button("Cancel") {
                    presentationMode.wrappedValue.dismiss()
                },
                trailing: Button("Save") {
                    submitThought()
                }
                .disabled(thoughtText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty || isSubmitting)
            )
        }
    }
    
    private func submitThought() {
        isSubmitting = true
        
        // Add thought via ThoughtStore
        thoughtStore.addThought(content: thoughtText)
        
        // Simulate network delay for demo purposes
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            isSubmitting = false
            presentationMode.wrappedValue.dismiss()
        }
    }
}

struct AddThoughtView_Previews: PreviewProvider {
    static var previews: some View {
        AddThoughtView()
            .environmentObject(ThoughtStore())
    }
}
