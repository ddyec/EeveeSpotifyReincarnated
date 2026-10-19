import SwiftUI
import UIKit

struct EeveeMiscellaneousSettingsView: View {
    @State private var cleanShareLinks = UserDefaults.cleanShareLinks
    @State private var blockRatingPrompts = UserDefaults.blockRatingPrompts

    var body: some View {
        List {
            Section(footer: Text("block_rating_prompts_footer".localized)) {
                Toggle("block_rating_prompts".localized, isOn: $blockRatingPrompts)
            }

            Section(footer: Text("clean_share_links_description".localized)) {
                Toggle("clean_share_links".localized, isOn: $cleanShareLinks)
            }

            RestartSection(visible: blockRatingPrompts != RatingPromptBlock.launchEnabled)

            SpacerView()
        }
        .eeveeSettingsStyle()
        .onChange(of: cleanShareLinks) { UserDefaults.cleanShareLinks = $0 }
        .onChange(of: blockRatingPrompts) { UserDefaults.blockRatingPrompts = $0 }
    }
}
