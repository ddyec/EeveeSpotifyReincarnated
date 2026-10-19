# EV1: EEVEE before spoti.pw

Based on SideloadLabs upstream Master, c211189324145d20a032eabc83f886ff8b38798d.
This dedicated branch identifies its package as 7.0.0+ev1.1 and its build as EV1.1.

## Ownership

spoti.pw owns appearance, lyrics, gestures, haptics, page decluttering, telemetry
blocking and user-selected remote flags. EV1 does not activate those EEVEE hook
groups and removes their settings entries. Their dormant source files remain to
avoid breaking shared types and make later upstream merges reviewable.

EV1 retains EEVEE's core playback/account response handling, ad and upsell
filtering, session protection, true shuffle, SponsorBlock, share-link cleaning,
rating-prompt blocking, CarPlay fix and its own small settings entry. Ad/upsell
filtering necessarily still removes promotional UI; it is not a theme/redesign.
Stock playback entitlements remain EEVEE's responsibility; EV1 removes its
forced AutoMix/crossfade feature flags and lyrics-sharing/layout flags.

The raw `lyricsSource=4` compatibility key is set before Orion initializes.
The Swift getter always returns `notReplaced`, even with imported old settings.
Both URLSession delegates now forward lyrics responses, including failures,
without fetching replacements, blocking on a semaphore or synthesizing a 200.

Whole configuration overwrite is disabled and hidden. EV1 uses a separate
customize-response cache key, so the first run cannot replay a snapshot created
by an older appearance/configuration profile. Existing account/login data is kept.

## Build order

1. Run **Build IPA (NO PATCH)** on this branch with no IPA URL to compile EV1's
   rootless deb and run companion regressions. This produces a tweak, not an IPA.
2. After the user provides a decrypted IPA URL, run that workflow with the URL.
   Its output is the EV1 intermediate IPA; use this artifact as stage two input.
3. The spoti.pw stage must use the official 1.0.0-beta.1 kit, not compile the
   public tag's obsolete 0.22 source or migrate the previous custom lyrics branch.
   Preserve EEVEE's dylib, framework, resources and load command, and load EEVEE
   before spotifyglass so Chroma sees the raw lyrics key during initialization.
   Validate this load order in the final Mach-O; if it cannot be established,
   stop before distributing a combined IPA. The key alone is not proof of
   load-order compatibility. The second-stage workflow is in `ddyec/spoti.pw`,
   branch `feat/ev1-official-beta-pipeline-20261019`; it establishes a strong
   dependency from spotifyglass to EEVEE and checks preserved resources.

The user supplied vanilla 9.1.88 and 9.1.90 plus an already patched 9.1.78.
This pipeline uses vanilla 9.1.90, which the official Chroma kit supports. EEVEE
documents 9.1.88 and selects the same hook family for 9.1.x; compilation and
packaging on 9.1.90 do not establish phone compatibility. Keep 9.1.88 for an
EEVEE-only comparison and do not double-patch the supplied 9.1.78.

## Acceptance

The Windows source audit is `python Tests/EV1Companion/test_source.py`.
The Action also compiles the real lyrics-source enum/getter with a Foundation
regression before compiling the tweak. A passing build does not establish phone
behavior. First install EV1 alone and check stock appearance, playback/login and
retained settings. Then check the combined IPA for a single UI/lyrics owner,
QQ-only/QQ-first lyrics, track changes and relaunch after importing old settings.
