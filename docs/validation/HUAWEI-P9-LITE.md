# Huawei P9 Lite — initial checks, 2026-10-20

Device reports VNS-L21, Android 10, LineageOS 17.1.0-vns (build dated 2023-08-12, security patch 2023-08-05), ARM64/ARMv7, MemTotal 1,821,440 kB. APK 0.4.4-dev. The user confirmed that the normal APK installation and prepared-ZIP import workflow works. This is human feedback, not an automated usability claim.

## Short stationary level checks

Both levels 1 and 13 loaded with synthesized music and effects and remained alive through the initial 30-second stationary checks. No invincibility or teleport fixture was used. This is not a playthrough, a sustained thermal test or a controller test.

| Scene | Native 1920×1080 output | Temporary 1280×720 output |
|---|---|---|
| Level 1 | 20.7 FPS first sample; 22.7 FPS next sample | 21.6 FPS first sample; 22.5 FPS next sample |
| Level 13 | 16.0 FPS initial sample | 16.6 FPS initial sample |

Samples contain 300 engine frames. First samples include transition/initialization stalls; they are not directly comparable to long warmed runs. Level 1 process PSS was 130,454 KiB at native output and 114,501 KiB at 720p. PSS is a point-in-time process measurement, not peak memory or total device use.

Reducing output resolution did not materially improve the observed level 1 frame rate. It reduced measured graphics/process memory. This suggests that output pixel fill alone is not the main bottleneck in that scene; CPU/update/draw-call costs still need profiling. Do not advertise a low-resolution mode as an established speed fix from this result.

Level 13 at 720p used 171,619 KiB process PSS. Both 720p level checks completed without a game-process crash. Raw evidence is stored locally in ignored `reports/huawei-initial-0.4.4/` and `reports/huawei-720p-0.4.4/`. Display size, game configuration and saves were restored after both runs.

## Bluetooth pairing, separate from gameplay

The user reports that Nova 2 Lite does not appear in Huawei's Bluetooth discovery list, despite a rapidly blinking yellow light and Bluetooth disabled on the previously paired Redmi. Android's Bluetooth manager records five service crashes; the log includes a SIGABRT in `bt_hci_thread` in the system Bluetooth process. Some recorded crashes preceded the level checks. This is evidence of system Bluetooth instability, not a demonstrated root cause or proof that the game/controller caused it.

The user additionally confirms that this same controller worked with this phone before installing the custom ROM. This makes the current ROM/Bluetooth stack or configuration a stronger suspect than a hardware incompatibility, but does not establish a specific software defect. No ROM flash, network reset, pairing deletion or controller firmware update was performed.

The manufacturer's [Android connection guide](https://gamesir.com/pages/tutorials-how-to-connect-nova-2-lite) specifies rapid yellow blinking and device name `GameSir-Nova 2 Lite`. Recommended next non-destructive check: toggle Bluetooth, then restart Huawei after the performance test finishes and retry discovery. Do not silently erase pairings or reset network settings. USB and successful Bluetooth gameplay remain untested on this phone.

## Polski

Użytkownik potwierdził instalację APK i import ZIP. Krótkie próby poziomów 1 i 13 zakończyły się bez awarii procesu gry, ale płynność jest niska. Zmniejszenie rozdzielczości nie poprawiło wyraźnie wyniku poziomu 1; potrzebne jest profilowanie. To nie jest pełne przejście gry. Systemowy Bluetooth kilkukrotnie się wysypał; przyczyna problemu parowania nie jest jeszcze ustalona.
