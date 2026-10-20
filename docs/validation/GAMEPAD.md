# Controller validation / Testy pada

Status: implemented and compiled. The user confirmed physical GameSir menu navigation on Huawei in red Switch mode. Gameplay actions, USB and sustained connection checks remain pending.

Huawei follow-up: exiting from the menu exposed a native shutdown crash. The log shows confirmation, `Terminating...`, then SIGSEGV from `exit()` in QuitGameDelegate. Android now stops the loop and returns normally instead of terminating the process inside EventMgr's callback. Touch textures, controller handles and held input are released before game teardown. Three successive menu exits/relaunches using SDL's virtual controller passed without fatal logs and with the activity finished. This automated exit check is distinct from the user's physical menu test. Local evidence: `reports/gamepad-quit-0.4.4/`; repeat with `tools/gamepad_quit_smoke.py`.

Implementation: SDL2 controller events, hotplug and a pinned Android subset of SDL_GameControllerDB. Android routes paired Bluetooth and USB input into the same SDL path. No application-level Bluetooth pairing is performed. Pair the controller in Android Settings first.

Previously observed on Redmi: GameSir Nova 2 Lite in a mode identified by Android as Wireless Controller (VID 054c, PID 09cc). This identifies the connected mode, not proof of correct button mapping. USB hardware testing remains pending. No controller was listed on the newly connected Huawei during the initial check.

| Action / Czynność | Expected / Oczekiwane |
|---|---|
| Left stick and D-pad | Both directions, diagonals, climbing and crouch; no movement at rest |
| A / bottom face | Jump; longer hold raises jump height |
| X / left face | Melee |
| B / right face, RT | Shoot; trigger releases correctly |
| Y / top face, LB, RB | Change weapon once per press |
| Start | Pause; release, press again to resume |
| Menu D-pad / stick | Selection and controlled repeat; A confirms, B goes back |
| Disconnect while moving | Movement stops; touch controls become available |
| Reconnect | No stuck action; release controls before continuing |
| Background and return | No held movement or jump carried into resumed game |
| Touch + pad | Releasing one source does not release a key still held by the other |

Record APK hash, device/Android, controller mode and transport for each run. Record failures as failures; do not mark a check passed from code inspection or a successful pairing. Never inject global Android key events for these checks: use the actual controller or app-local diagnostics.

## Natural playthrough / Zwykłe przejście

For each level 1–14, record entry, checkpoint reload, death/retry, enemy encounters, moving platforms/traps, level completion and progression to the next map. Include the level number and approximate location for every failure. Separate normal play from invincibility, teleports and isolated diagnostic arenas. A successful load is not a completed level. The full natural playthrough remains pending.
