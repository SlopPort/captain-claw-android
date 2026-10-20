# Drabiny / Ladder investigation

Reported by the user on the first ladder of level 1: holding Up after reaching the top kept the climbing animation active. The user subsequently confirmed that configurable controller bindings work well. PAD previously covered health; version 0.4.6 moves it to the bottom centre.

## Evidence and change

Upstream PhysicsComponent contained an explicit TODO to disable upward climbing at the top and a commented-out implementation. Attachment checked horizontal alignment but not whether any ladder extended above the actor's feet. The body/foot sensor could still overlap the ladder while standing on its one-way cap, so held Up reattached the actor repeatedly.

An isolated production-physics ladder reproduced more than a cosmetic problem. Its cap was at y=768; standing actor y was 712.6. While holding Up the baseline sample reached y=675.0 with animation `climb`; pressing Up again after releasing produced y=703.1. The character was being pulled above the cap and falling back. Local baseline: `reports/ladder-baseline/`.

The fix checks active actor bounds against every overlapping ladder segment. If none extends above the feet (with two pixels of Box2D/rounding tolerance), ascent ends, gravity is restored and the climbing animation stops. Up cannot reattach from that standing position. Down retains its original attachment path. Checking all segments preserves connected stacks of ladder tiles.

The isolated fixed sample stood at y=712.6, ground contact present, climbing false. On the real first level, the leftmost ladder cap from map metadata is x=1408, y=4352; the centred actor stood at x=1440, y=4296.6. Holding and pressing Up again kept that position with climbing false. A longer hold can enter the existing `lookup` animation. Descent through the real ladder segments, sideways movement from the cap and Up+Jump from the cap were observed separately.

## Limits and test-fixture corrections

This is a verified OpenClaw defect and port change; exact behavior of the shipped Windows game was not established. A design document or remake is not a substitute for a direct original-game comparison. No original assets were changed or redistributed for this fix.

One attempted midair teleport fixture fell below the ladder before climbing began; it was retained as a failed setup (`ladder-level1-edges-0.4.6`). The later real-map fixture starts on the cap, descends, then climbs back rather than relying on a midair placement. Late jump snapshots also sometimes caught the return/descent instead of the jump's peak. The test was strengthened to sample maximum rise each frame and compare the jump with the stationary pre-jump position. Failed intermediate reports were not presented as passed physics tests.

Controlled fixtures use app-local diagnostic commands; real-map tests enable temporary player invulnerability and teleport placement. Configuration and saves are restored. These are not a natural playthrough. Reproduce with `python tools/ladder_smoke.py --expect-fixed --first-map-ladder --report ladder-review`.

Final run: `reports/ladder-level1-verified-0.4.6/`, APK SHA-256 `6ce91b1ee6465dab708a9f0171ff6deb7f4f8f0b625cd71be9cfae33dd8cef8e`. All final assertions passed. The per-frame ladder-jump trace measured 145.1 px rise and one jump; late endpoint frames were not used as evidence of failure. The test also verified re-ascent after descending real tile segments, horizontal movement off the cap, and Up+Jump from the top. The saved screen check confirms that health is unobstructed and PAD is at the bottom centre. Physics changes are in the reproducible OpenClaw patch.

## Additional bug found: held menu directions

The controller already emitted timed directional repeats, but ScreenElementMenuPage discarded repeat events. Android menus now accept repeated Up/Down while continuing to reject repeated confirmation/page actions. `reports/gamepad-menu-repeat-0.4.6/` recorded eight selection changes on the same page during one held Down input, with no confirmation and no exit. This is a separate menu fix, not a ladder-physics change.

## Polski

Potwierdzono błąd odziedziczonej fizyki: trzymanie góry na szczycie ponownie zaczepiało Pazura o drabinę i podciągało go ponad podest. Poprawka kończy wspinanie i blokuje zaczepienie od góry, zachowując schodzenie. Próby obejmują kontrolowaną drabinę oraz prawdziwą drabinę poziomu 1. Nie potwierdzono jeszcze dokładnej zgodności z zachowaniem oryginalnego wydania Windows ani pełnego przejścia wszystkich poziomów.
