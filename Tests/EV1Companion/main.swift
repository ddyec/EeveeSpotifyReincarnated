import Foundation

extension UserDefaults {
    static let container = UserDefaults(suiteName: "EV1CompanionRegression")!
}

let domain = "EV1CompanionRegression"
defer { UserDefaults.container.removePersistentDomain(forName: domain) }
UserDefaults.container.removePersistentDomain(forName: domain)
precondition(!UserDefaults.lyricsSource.isReplacingLyrics, "fresh installs must leave lyrics alone")
for raw in [0, 1, 2, 3, 4, 5, 999] {
    UserDefaults.container.set(raw, forKey: "lyricsSource")
    precondition(UserDefaults.lyricsSource == .notReplaced, "old preferences enabled lyrics")
}
for source in LyricsSource.allCases {
    UserDefaults.lyricsSource = source
    precondition(UserDefaults.lyricsSource == .notReplaced)
    precondition(UserDefaults.container.integer(forKey: "lyricsSource") == 4,
                 "Chroma reads the raw interop key")
}
print("PASS: EV1 refuses fresh, stale and imported lyrics-source settings")
