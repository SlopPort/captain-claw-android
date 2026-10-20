# Controller validation / Testy pada

Status: implemented and compiled. The user confirmed physical GameSir menu navigation on Huawei in red Switch mode. Gameplay actions, USB and sustained connection checks remain pending.

Huawei follow-up: exiting from the menu exposed a native shutdown crash. The log shows confirmation, `Terminating...`, then SIGSEGV from `exit()` in QuitGameDelegate. Android now stops the loop and returns normally instead of terminating the process inside EventMgr's callback. Touch textures, controller handles and held input are released before game teardown. Three successive menu exits/relaunches using SDL's virtual controller passed without fatal logs and with the activity finished. This automated exit check is distinct from the user's physical menu test. Local evidence: `reports/gamepad-quit-0.4.4/`; repeat with `tools/gamepad_quit_smoke.py`.

Level 1 pause follow-up: the user reported a freeze when opening the in-game menu. Logs showed rendering continuing, with controller events ceasing after pause. ScreenElementMenu calls SetRunning(false) while GameState stays IngameRunning; controller context incorrectly returned 0 (input disabled). That combination now routes to menu context 2, allowing release gating, navigation and resume. Three virtual-controller cycles on the real level passed: pause, held-Start protection, menu direction, resume. Local evidence: `reports/gamepad-pause-0.4.4/`; reproduce with `tools/gamepad_pause_smoke.py`. Physical controller confirmation after this fix remains pending.

Implementation: SDL2 controller events, hotplug and a pinned Android subset of SDL_GameControllerDB. Android routes paired Bluetooth and USB input into the same SDL path. No application-level Bluetooth pairing is performed. Pair the controller in Android Settings first.

Previously observed on Redmi: GameSir Nova 2 Lite in a mode identified by Android as Wireless Controller (VID 054c, PID 09cc). This identifies the connected mode, not proof of correct button mapping. USB hardware testing remains pending. No controller was listed on the newly connected Huawei during the initial check.

| Action / Czynność | Expected / Oczekiwane |
|---|---|
| Left stick and D-pad | Both directions, diagonals, climbing and crouch; no movement at rest |
| A / bottom face | Jump; longer hold raises jump height |
| X / left face | Melee |
| Android BUTTON_B, or a configured trigger | Shoot; configured trigger releases correctly |
| Android BUTTON_Y, or a configured shoulder | Change weapon once per press |
| Start | Pause; release, press again to resume |
| Menu D-pad / stick | Selection and controlled repeat; A confirms, B goes back |
| Disconnect while moving | Movement stops; touch controls become available |
| Reconnect | No stuck action; release controls before continuing |
| Background and return | No held movement or jump carried into resumed game |
| Touch + pad | Releasing one source does not release a key still held by the other |

Record APK hash, device/Android, controller mode and transport for each run. Record failures as failures; do not mark a check passed from code inspection or a successful pairing. Never inject global Android key events for these checks: use the actual controller or app-local diagnostics.

## Version 0.4.5: configurable physical buttons

The user reported no sword attack on any physical button. Earlier logs contained jump/fire/weapon actions but no attack=1; the exact original hardware mapping defect was not isolated. Android button events now enter an app-local JNI/SDL queue before device-specific SDL button translation, and the user can capture the desired physical key in the PAD screen. Axes/D-pad remain handled by SDL. The game combines all input through PlatformInput ownership; a Java event is not also dispatched as an SDL controller button. Bindings are global for this installation, not per-device profiles.

Automated capture test on Huawei: open PAD, choose sword, capture Android BUTTON_L1 (102), save, return to the game, reload the file and dispatch that key through GameActivity/JNI. Native logs show attack=1, fire=0, followed by Soldier defeated in an isolated passive fixture. This is evidence of UI capture, persistence, routing and actual sword damage, not confirmation that every physical GameSir button now works. Settings/config/saves were restored after the test. Local evidence: `reports/controller-bindings-0.4.5/`.

Build the capture test with `-PtestRunner=pl.pazur.port.ControllerBindingsTest :app:assembleDebugAndroidTest`, install both APKs and run `python tools/controller_bindings_smoke.py`. Without that property the default test runner remains JumpTouchTest. `tools/gamepad_pause_smoke.py --raw-buttons` exercises pause/resume via raw Android codes; the ordinary mode retains SDL virtual-controller button coverage. [User binding guide](../CONTROLLER.md).

The raw-button pause test passed three cycles on Huawei. Touch instrumentation also completed, with useful short jumps and full held jumps, but the host regression failed its 65 ms latency threshold: first takeoff 124 ms, subsequent measurements 47–51 ms. There is no pre-0.4.5 Huawei touch latency comparison establishing whether this is a new regression. This remains an open performance finding, not a fully passed touch regression. Raw evidence: `reports/jump-touch-huawei-0.4.5/`.

## Natural playthrough / Zwykłe przejście

For each level 1–14, record entry, checkpoint reload, death/retry, enemy encounters, moving platforms/traps, level completion and progression to the next map. Include the level number and approximate location for every failure. Separate normal play from invincibility, teleports and isolated diagnostic arenas. A successful load is not a completed level. The full natural playthrough remains pending.
