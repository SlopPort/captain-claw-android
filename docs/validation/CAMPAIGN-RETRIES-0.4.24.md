# Natural campaign retries

> Historical validation record. Results apply to the builds and scenarios named here, not automatically to the latest APK. See the [README](../../README.md) for current project status.

OpenAI Codex (LLM), 2026-10-23. Huawei Android 10, existing 0.4.24-dev APK:
`583ec1d605527ba812e7da3da510a52dc4e08a2cc94f84c4733592051f2cc0a2`.

Six further attempts (`natural-campaign-huawei-0.4.24-resume2` through `resume7`
in ignored local reports) resumed the same unmodified game-written L1 checkpoint
1. Each retained its original resources. These were ordinary key inputs and
read-only observations, not teleports, immunity, health edits or level fixtures.
No natural level exit or checkpoint 2 was reached. Earlier farther route coverage
in [the previous report](HUAWEI-CAMPAIGN-0.4.24.md) remains the furthest evidence.

The crumbling-peg chain repeatedly passed with HP100. Later failures included:

- Standing fire at the upper ladder left too little health for the carrier route.
- Down at the ladder cap descended the ladder instead of crouching. The resulting
  return to enemy fire was a driver error; it does not establish a game defect.
- Bypassing the upper Soldier left him firing during the carrier wait.
- Crouching on the actual ledge killed that Soldier in another attempt, but the
  first carrier jump missed. The old driver continued from the lower floor.
- Knockback left x8257.9, outside the intended ladder alignment, so a blind Up
  input did not climb. In the last attempt, ordinary correction reached the cap
  with HP90, but a projectile struck immediately after the jump command; Claw
  returned to the lower floor. A normal recovery climb reached the cap again,
  then subsequent fire exhausted health. Switching to an owned magic weapon
  during hurt recovery did not consume a shot; it was not a successful attack.

The first-carrier evidence also exposed host-input timing limitations: a sampled
carrier x8759.8 was followed by native jump execution when the carrier had already
advanced beyond x8780. This is an automation timing problem, not proof of faulty
platform physics. A new experimental `campaign_first_carrier_step.py` uses an
earlier window, rejects a wrong starting ledge and checks upper height/grounded
samples before declaring success. Syntax checking passed; its new boarding window
has **not yet been validated on the device**. It must not be cited as a passing
carrier test. Future work must observe health, alignment and actual landings
instead of blindly replaying the remainder of a failed route.

No Fatal signal / FATAL EXCEPTION was identified in these attempts. Rejections
after Game Over are tool errors, not crash evidence. The tool may still wait for
its death-transition timeout when Game Over is terminal; improve this reporting.
All owners ended. The final save and configuration pulled from Huawei matched
the last owner's original backups byte for byte (`resume7/restoration.json`).
No Redmi operation, ADB-server restart or USB/network change was requested.
No APK, gameplay balance, physics or FPS optimization changed in this batch.
