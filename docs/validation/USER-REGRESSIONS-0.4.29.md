# User regressions 0.4.29 / Zgłoszenia użytkownika

**Follow-up, 2026-10-24:** the human later made Redmi available. [Separate exact-version checks and cleanup](REDMI-0.4.29.md) passed there. The Huawei-only scope below remains the record of the original 2026-10-23 batch.

OpenAI Codex (LLM), 2026-10-23. Only Huawei P9 Lite / Android 10 was accessed in
this batch. Redmi belongs to another task and was not queried or updated.
No natural campaign traversal. Virtual SDL/raw input tests do not prove physical
Bluetooth/USB controller transport.

Final debug 0.4.29-dev/code41, ARM64+ARMv7 APK SHA-256:
`39c004705c2e0ee57cdd6a23e0ebbc5d3ca35ab981581d766568b7431c67bdbc`.
Local `dist/kapitan-pazur-0.4.29-dev.apk`. Huawei runs ARM64. Config, progress and
controller bindings survived in-place updates byte for byte. Redmi remains on its
previous version. No new signed-release runtime or emulator certification is
assigned to this native-code update; earlier compatibility reports keep their
own exact-version scope. This is not 1.0.

## Pause

The real profile assigned Pause to Android Back/code4. GameActivity consumes raw
Android gamepad buttons before SDL remapping, so physical Start/code108 was not
covered by the SDL START fallback. Baseline virtual raw108 failed to pause.
Raw Start now remains available as a menu key alongside a custom Pause binding;
the profile itself is not overwritten. Test holds/releases Start, pauses/resumes
three times and checks context changes. This is app-local routing coverage, not
a fresh physical-controller pass. Start is reserved for menu use; avoid assigning
another gameplay action to it.

## Catnip pickup hitch

Console-triggered Catnip on 0.4.27 reproduced ~142/151 ms slow frames at acquisition.
Music loading was synchronous on the game thread. The level and powerup MIDI songs
are now prepared during level loading. A bounded cache retains at most three
prepared songs; immutable owned bytes outlive each SDL_mixer song. Eviction never
frees the currently playing song; termination frees the cache before audio closes.
No asynchronous access to engine resources was introduced. The load cost moves
to the loading screen rather than the pickup.

Intermediate 0.4.28 SHA
`091b31cf833efb8b2b524a8f22991a4de80dfa9ee583b3e1b49c1f5852f60602`
passed acquisition, expiry and reacquisition at 1/1/1 ms for music switching, with
PCM output and no preparation during that gameplay interval. This measures the
music operation, not every frame or an actual collected pickup. Final 0.4.29 independently passed all three pause cycles and music transitions at
2/1/1 ms, with PCM output and no in-game preparation. These are music-operation
timings, not a guarantee that every game frame takes at most 2 ms.

## Game Over crash and wording

Android retained a real 0.4.27 native SIGABRT: MoveToMenuItemIdx asserted
“Could not find any button to switch focus to”. The stack includes controller
input. The text-only Game Over page has no focusable buttons; a directional input
can still arrive from the pad while the player touches the display.

Three ordinary touch-only deaths and two Catnip-plus-six-tap trials passed on
0.4.27. These did not cover the crashing direction input. A separate old-code
0.4.28 baseline reproduced the exact focus assertion with virtual-pad Down.
The fix preserves text state when there is no destination and bounds the search
without relying on assertions. This also avoids an endless search with NDEBUG.
The no-active-item case remains valid for Enter/Escape keyboard actions.

The final regression passed both Down and Up on Game Over, then touched to return
to the main menu. Two additional final-version Catnip-plus-six-tap death cycles
also passed without native/Java fatal logs. This reproduces and fixes a matching stored crash mechanism;
it does not prove every possible crash near death has been eliminated.
The label now reads “Koniec gry / Dotknij ekranu: menu główne” or
“Game Over / Tap screen: main menu”. It does not promise an immediate new game.

## Repeated hits below Soldier

An active level-one Soldier on an isolated 32 px step reproduced the complaint:
100 ms sword taps sent after an observed hit could be lost entirely during hurt.
In the two standing trials Claw fell from HP90 to20 without an attack animation.
Damage intervals were roughly 630 ms, with recovery-to-stand windows between
hurt animations; this is repeated interruption, not proof of a permanently frozen
state. Longer retreat input escaped in those fixtures. Source/contact traces
showed overlapping enemy attack and hero body rectangles.

Android now retains one melee tap for at most 400 ms during TakingDamage, consumes
it at the end of the hurt animation and clears it on death. Wall-clock expiry
prevents a long pause storing a surprise future attack. No attack runs during
hurt; damage, enemy AI, immunity timing and hitbox sizes are unchanged. This is
an intentional input accommodation, **not verified original-Windows behavior**.
No original Monolith source or matched original-game capture was available.

A diagnostic scheduler observes the next real health loss and emits an ordinary
100 ms SDL key tap. It does not call attack directly or edit health during the
observation. The regression requires both buffering and consumption plus an attack
area. The initial left-side case attacked away from the enemy because its tiny
turn input was itself sent during hurt: retained as tap-handling evidence, not a
successful strike. The follow-up faces the enemy before fixture creation and
requires a recorded contact with Soldier on both sides. Both follow-up cases
passed: buffered tap consumed, Soldier HP10 ->0 with Claw as source, hero HP90
before arming ->80 at the end. The tap itself occurs after the next real enemy
hit. This remains isolated
terrain coverage; it does not establish every natural stair encounter is fair.

## Evidence and reproduction

Builds assembleDebug/assembleDebugAndroidTest/lintDebug passed for both ARM ABIs;
zero lint errors, 29 retained warnings. Existing C++ warnings were not suppressed.
Public scripts: pause_powerup_smoke.py, game_over_pad_navigation_smoke.py,
game_over_touch_smoke.py (--powerup/--rapid-taps), melee_recovery_smoke.py.
Always set ANDROID_SERIAL explicitly to an allocated device. CampaignSession
restores original config/progress and now checks restored bytes before reporting
completion. Use fresh report names and your own legitimate game data. Do not
restart the shared ADB server or change Huawei USB tethering.

Private prefixes: user-pause-catnip-huawei-0.4.27,
game-over-user-huawei-0.4.27, game-over-powerup-rapid-huawei-0.4.27,
game-over-pad-focus-huawei-0.4.28-baseline,
game-over-pad-focus-huawei-0.4.29-fixed,
stagger-soldier-below-huawei-0.4.28, melee-recovery-huawei-0.4.29,
melee-recovery-huawei-0.4.29-r2, pause-powerup-huawei-0.4.29.
Raw crash reports contain private paths/device metadata and stay outside Git.

## Polski

Naprawiono brak pauzy Startem przy własnym mapowaniu, koszt przełączenia muzyki
złotej myszy oraz odtworzoną awarię kierunków pada na tekstowym ekranie końca gry.
Komunikat jasno opisuje powrót do menu. Krótkie naciśnięcie szabli podczas trafienia
jest teraz zapamiętywane do końca animacji, maksymalnie 400 ms. To udogodnienie
portu, bez powiększania hitboxów i bez twierdzenia o identyczności z oryginałem.
Próby dotyczą Huawei i izolowanych scen; naturalna kampania pozostaje zadaniem
człowieka. Redmi nie był używany. Własny klucz podpisu nadal jest prywatny.
