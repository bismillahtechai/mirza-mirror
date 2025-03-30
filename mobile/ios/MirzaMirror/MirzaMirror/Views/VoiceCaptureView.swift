import SwiftUI
import AVFoundation

struct VoiceCaptureView: View {
    @Environment(\.presentationMode) var presentationMode
    @EnvironmentObject var apiService: APIService
    @State private var isRecording = false
    @State private var audioRecorder: AVAudioRecorder?
    @State private var recordingURL: URL?
    @State private var recordingTime: TimeInterval = 0
    @State private var timer: Timer?
    @State private var isUploading = false
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Spacer()
                
                // Recording indicator
                if isRecording {
                    VStack {
                        Text("Recording...")
                            .font(.title)
                            .foregroundColor(.red)
                        
                        Text(timeString(from: recordingTime))
                            .font(.system(size: 60, weight: .bold, design: .monospaced))
                            .foregroundColor(.red)
                            .padding()
                        
                        // Waveform visualization (simplified)
                        HStack(spacing: 4) {
                            ForEach(0..<20) { _ in
                                RoundedRectangle(cornerRadius: 3)
                                    .frame(width: 6, height: CGFloat.random(in: 10...50))
                                    .foregroundColor(.red)
                                    .animation(.easeInOut(duration: 0.2).repeatForever(), value: isRecording)
                            }
                        }
                        .padding()
                    }
                } else {
                    VStack {
                        Image(systemName: "mic.circle")
                            .font(.system(size: 100))
                            .foregroundColor(.blue)
                        
                        Text("Tap to Start Recording")
                            .font(.title2)
                            .foregroundColor(.secondary)
                    }
                }
                
                Spacer()
                
                // Error message
                if let error = errorMessage {
                    Text(error)
                        .foregroundColor(.red)
                        .padding()
                }
                
                // Recording button
                Button(action: {
                    if isRecording {
                        stopRecording()
                    } else {
                        startRecording()
                    }
                }) {
                    ZStack {
                        Circle()
                            .fill(isRecording ? Color.red : Color.blue)
                            .frame(width: 80, height: 80)
                        
                        if isRecording {
                            RoundedRectangle(cornerRadius: 4)
                                .fill(Color.white)
                                .frame(width: 30, height: 30)
                        } else {
                            Image(systemName: "mic")
                                .font(.system(size: 40))
                                .foregroundColor(.white)
                        }
                    }
                }
                .disabled(isUploading)
                
                if !isRecording && recordingURL != nil {
                    Button("Upload Recording") {
                        uploadRecording()
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(isUploading)
                    .padding()
                }
                
                if isUploading {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle())
                        .scaleEffect(1.5)
                        .padding()
                }
            }
            .padding()
            .navigationTitle("Voice Capture")
            .navigationBarItems(trailing: Button("Cancel") {
                presentationMode.wrappedValue.dismiss()
            })
            .onDisappear {
                if isRecording {
                    stopRecording()
                }
                timer?.invalidate()
            }
        }
    }
    
    private func startRecording() {
        let audioSession = AVAudioSession.sharedInstance()
        
        do {
            try audioSession.setCategory(.playAndRecord, mode: .default)
            try audioSession.setActive(true)
            
            // Create recording URL in temp directory
            let documentsPath = FileManager.default.temporaryDirectory
            let audioFilename = documentsPath.appendingPathComponent("\(UUID().uuidString).m4a")
            
            // Recording settings
            let settings = [
                AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
                AVSampleRateKey: 44100,
                AVNumberOfChannelsKey: 2,
                AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
            ]
            
            // Create recorder
            audioRecorder = try AVAudioRecorder(url: audioFilename, settings: settings)
            audioRecorder?.record()
            
            recordingURL = audioFilename
            isRecording = true
            recordingTime = 0
            
            // Start timer to update recording time
            timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
                recordingTime += 0.1
            }
            
        } catch {
            errorMessage = "Failed to start recording: \(error.localizedDescription)"
        }
    }
    
    private func stopRecording() {
        audioRecorder?.stop()
        isRecording = false
        timer?.invalidate()
    }
    
    private func uploadRecording() {
        guard let url = recordingURL else {
            errorMessage = "No recording to upload"
            return
        }
        
        isUploading = true
        
        do {
            let audioData = try Data(contentsOf: url)
            
            // Use APIService to upload
            // This would be implemented with Combine in a real app
            // For simplicity, we're using a mock implementation
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                isUploading = false
                presentationMode.wrappedValue.dismiss()
            }
            
        } catch {
            isUploading = false
            errorMessage = "Failed to upload recording: \(error.localizedDescription)"
        }
    }
    
    private func timeString(from timeInterval: TimeInterval) -> String {
        let minutes = Int(timeInterval) / 60
        let seconds = Int(timeInterval) % 60
        let tenths = Int((timeInterval - floor(timeInterval)) * 10)
        return String(format: "%02d:%02d.%01d", minutes, seconds, tenths)
    }
}

struct VoiceCaptureView_Previews: PreviewProvider {
    static var previews: some View {
        VoiceCaptureView()
            .environmentObject(APIService())
    }
}
