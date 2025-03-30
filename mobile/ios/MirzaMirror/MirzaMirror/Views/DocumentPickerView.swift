import SwiftUI
import UniformTypeIdentifiers

struct DocumentPickerView: View {
    @Environment(\.presentationMode) var presentationMode
    @EnvironmentObject var apiService: APIService
    @State private var showingDocumentPicker = false
    @State private var selectedDocument: UIDocument?
    @State private var documentData: Data?
    @State private var documentName: String = ""
    @State private var documentType: String = ""
    @State private var isUploading = false
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Spacer()
                
                // Document selection area
                VStack {
                    if let document = selectedDocument {
                        VStack {
                            Image(systemName: documentTypeIcon(for: documentType))
                                .font(.system(size: 60))
                                .foregroundColor(.blue)
                            
                            Text(document.fileURL.lastPathComponent)
                                .font(.headline)
                                .padding()
                            
                            Text("Ready to upload")
                                .foregroundColor(.green)
                        }
                        .padding()
                        .background(Color(.systemGray6))
                        .cornerRadius(12)
                        .padding()
                    } else {
                        VStack {
                            Image(systemName: "doc.badge.plus")
                                .font(.system(size: 80))
                                .foregroundColor(.blue)
                            
                            Text("Select a Document")
                                .font(.title2)
                                .padding()
                            
                            Text("Tap the button below to choose a document to upload")
                                .multilineTextAlignment(.center)
                                .foregroundColor(.secondary)
                                .padding(.horizontal)
                        }
                        .padding()
                    }
                }
                
                Spacer()
                
                // Error message
                if let error = errorMessage {
                    Text(error)
                        .foregroundColor(.red)
                        .padding()
                }
                
                // Document picker button
                Button(action: {
                    showingDocumentPicker = true
                }) {
                    HStack {
                        Image(systemName: "doc.badge.plus")
                        Text(selectedDocument == nil ? "Select Document" : "Change Document")
                    }
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                }
                .disabled(isUploading)
                .padding()
                
                // Upload button
                if selectedDocument != nil {
                    Button("Upload Document") {
                        uploadDocument()
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(isUploading)
                    .padding(.bottom)
                }
                
                if isUploading {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle())
                        .scaleEffect(1.5)
                        .padding()
                }
            }
            .padding()
            .navigationTitle("Document Upload")
            .navigationBarItems(trailing: Button("Cancel") {
                presentationMode.wrappedValue.dismiss()
            })
            .sheet(isPresented: $showingDocumentPicker) {
                DocumentPicker(selectedDocument: $selectedDocument, documentData: $documentData, documentName: $documentName, documentType: $documentType)
            }
        }
    }
    
    private func uploadDocument() {
        guard let data = documentData, !documentName.isEmpty, !documentType.isEmpty else {
            errorMessage = "Document data is missing"
            return
        }
        
        isUploading = true
        errorMessage = nil
        
        // In a real app, we would use the APIService to upload the document
        // For this demo, we'll simulate a network request
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            isUploading = false
            presentationMode.wrappedValue.dismiss()
        }
    }
    
    private func documentTypeIcon(for type: String) -> String {
        switch type {
        case "image/jpeg", "image/png", "image/heic":
            return "photo"
        case "application/pdf":
            return "doc.text"
        case "text/plain":
            return "doc.text"
        case "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return "doc.text"
        default:
            return "doc"
        }
    }
}

struct DocumentPicker: UIViewControllerRepresentable {
    @Binding var selectedDocument: UIDocument?
    @Binding var documentData: Data?
    @Binding var documentName: String
    @Binding var documentType: String
    
    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        let supportedTypes: [UTType] = [
            .pdf,
            .image,
            .text,
            .plainText,
            .jpeg,
            .png
        ]
        
        let picker = UIDocumentPickerViewController(forOpeningContentTypes: supportedTypes)
        picker.allowsMultipleSelection = false
        picker.delegate = context.coordinator
        return picker
    }
    
    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, UIDocumentPickerDelegate {
        let parent: DocumentPicker
        
        init(_ parent: DocumentPicker) {
            self.parent = parent
        }
        
        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            guard let url = urls.first else { return }
            
            // Create a document object
            let document = UIDocument(fileURL: url)
            parent.selectedDocument = document
            parent.documentName = url.lastPathComponent
            
            // Determine content type
            let uti = UTType(filenameExtension: url.pathExtension)
            parent.documentType = uti?.preferredMIMEType ?? "application/octet-stream"
            
            // Load document data
            do {
                let data = try Data(contentsOf: url)
                parent.documentData = data
            } catch {
                print("Error loading document data: \(error)")
            }
        }
    }
}

struct DocumentPickerView_Previews: PreviewProvider {
    static var previews: some View {
        DocumentPickerView()
            .environmentObject(APIService())
    }
}
