import SwiftUI
import Combine

@main
struct MirzaMirrorApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(ThoughtStore())
                .environmentObject(APIService())
        }
    }
}
