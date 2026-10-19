import Foundation

extension UserDefaults {
    private static let lyricsSourceKey = "lyricsSource"
    
    static var lyricsSource: LyricsSource {
        get { .notReplaced }
        set {
            // Dedicated companion build: a stale UI or imported preference must
            // never enable a second lyrics engine.
            container.set(LyricsSource.notReplaced.rawValue, forKey: lyricsSourceKey)
        }
    }
}
