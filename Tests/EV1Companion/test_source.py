"""Reject reintroduction of the EEVEE hooks that compete with spoti.pw."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
src = root / 'Sources/EeveeSpotify'
tweak = (src / 'Tweak.x.swift').read_text(encoding='utf-8')
for call in (
    'activateTheme', 'activateLiquidGlass', 'activatePlayerGestures',
    'activatePlayerHaptics', 'activateHomeDeclutter', 'activateGlassCustomTabs',
    'activateHomeGradient', 'activateArtistHides', 'activatePlaylistHides',
    'activateRemoteFlags', 'activateTelemetryBlock', 'activateEeveeCrossfadeForce',
    'activateKaraokeHooks',
):
    assert not re.search(r'\b' + call + r'\s*\(', tweak), call
for group in ('BaseLyricsGroup', 'V91LyricsGroup', 'ModernLyricsGroup',
              'LegacyLyricsGroup', 'LyricsErrorHandlingGroup', 'DarkPopUps', 'HideJam'):
    assert not re.search(r'\b' + group + r'(?:\(\))?\.activate\(', tweak), group
for call in ('activateEeveePremiumForce', 'activateEeveeAdBlockerExtended',
             'activateSessionLogoutProtection', 'activateSponsorBlock',
             'activateRatingPromptBlock'):
    assert re.search(r'\b' + call + r'\(', tweak), call

for name in ('DataLoaderServiceHooks.x.swift', 'HttpClientURLSessionHooks.x.swift'):
    text = (src / name).read_text(encoding='utf-8')
    # Both 200 completion and non-200 response callbacks must be pass-through.
    for forbidden in ('getLyricsDataForCurrentTrack', 'url.isLyrics', 'DispatchSemaphore'):
        assert forbidden not in text, (name, forbidden)
    assert 'didReceiveResponse: response, completionHandler: handler)' in text

patcher = (src / 'Premium/Helpers/SpotifyResponsePatcher.swift').read_text(encoding='utf-8')
assert 'BaseLyricsGroup' not in patcher and 'url.isLyrics' not in patcher
settings = (src / 'Settings/Views/EeveeSettingsView.swift').read_text(encoding='utf-8')
for name in ('EeveeLyricsSettingsView()', 'AppearanceSettingsView()',
             'EeveeUISettingsView()', 'EeveeAppIconPickerView()',
             'SpotifyFeaturesView()', 'FlagBrowserView()'):
    assert name not in settings, name
defaults = (src / 'Shared/Models/Extensions/UserDefaults+Extension.swift').read_text(encoding='utf-8')
assert '"eeveeEV1CachedCustomizeData"' in defaults
assert '"eeveeCachedCustomizeData"' not in defaults
getter = re.search(r'static var overwriteConfiguration: Bool \{\s*get \{(.*?)\}', defaults, re.S)
assert getter and re.search(r'\bfalse\b', getter[1])
config = (src / 'Premium/DynamicPremium+ModifyingFunctions.swift').read_text(encoding='utf-8')
assert 'name: "should_nova_scroll_use_scrollsita"' not in config
assert 'scope: "ios-feature-lyrics"' not in config
assert 'name: "automix_enabled"' not in config
assert 'name: "crossfade_enabled"' not in config
ctor = (root / 'Sources/EeveeSpotifyC/Tweak.m').read_text(encoding='utf-8')
assert ctor.index('setInteger:4 forKey:@"lyricsSource"') < ctor.index('        orion_init();')
print('PASS: EV1 appearance, lyrics delegates, stale configuration and retained services')
