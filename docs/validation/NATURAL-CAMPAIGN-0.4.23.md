# Natural campaign attempt — 0.4.23

Status: **incomplete; level 1 not completed**. Work and observations by OpenAI
Codex (LLM). Do not substitute this for a campaign pass or a 1.0 release gate.

APK: `7b428f35c357bebb26757ae9bac1d8153ee5136ecc525783be646016fe42379c`.
Device: Redmi Note 8, Android 16. The controlled test save begins with normal
level-one resources: health 100, lives 3, pistol 10, magic 5, dynamite 3.
No teleport, protection, ammo/health edits, spawned shots or added terrain were
used within these natural attempts. Read-only local map inspection assisted
route planning. Diagnostics were enabled; this was not a performance benchmark.

The second attempt traversed the first ladder and early platforms, collected
catnip and the respawn flag, returned along the lower route after missed jumps,
and used the ordinary End Life menu three times to return to the flag. Those
choices consumed lives normally, eventually leaving zero spare lives. They were
not save edits, but they are also not successful traversal of the missed gaps.

A crouching pistol shot at the real upper-route powder keg caused an actual
explosion, reduced hero health by 50, and defeated the nearby officer. The fixed
process survived. The player later missed the moving platform again and landed
on the lower floor. An observed natural jump had 34 ms takeoff latency and a
155-pixel rise with a 600 ms hold: the input was accepted and reached full height.
This does not establish successful boarding or original-game timing parity.

No persistent disk checkpoint was reached. The first flag is a runtime respawn
point; these attempts do not provide a resumable campaign save at that position.
The run was stopped before separately investigating boarding with a controlled
fixture. Both original user files were pulled again after restoration and
compared byte for byte: configuration PASS, saves PASS.

Raw evidence stays local in ignored
`reports/natural-campaign-0.4.23-run1` and
`reports/natural-campaign-0.4.23-run2`: command ledger, native logs, per-step
screenshots, ordinary menu actions and `restoration.json`. Earlier misses and
test-driver failures remain retained. They must not be counted as game bugs
without a reproducible game-side cause. In particular, death fade temporarily
stops physics for about six seconds in the observed sequence; the initial
driver's early rejection was corrected by bounded retry, not by changing the game.

Next: measure real hero/platform trajectories in a separately labelled fixture,
then repeat natural boarding and continue through the first persistent checkpoint.
All 14 levels, normal resource balance, bosses and final ending remain open.
