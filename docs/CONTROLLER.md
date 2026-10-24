# Controller setup

Since 0.4.29, Android **BUTTON_START** remains a pause/menu fallback alongside custom bindings. Reserve it for menu use rather than assigning it another gameplay action. Printed labels depend on controller mode. [Regression evidence](validation/USER-REGRESSIONS-0.4.29.md).

1. Pair the controller in Android Settings and open the game. The test Huawei paired a GameSir Nova 2 Lite in red Switch mode as Pro Controller; names can differ by controller mode/device.
2. Tap **PAD** in the game to open controller settings. Its current placement can be checked against the [UI notes](GAME-OVER-UI.md).
3. Choose an action such as **Sword attack**, release the controls, then press the desired button or trigger.
4. Changes save automatically. If that button already belongs to another action in the same group, their assignments swap. Gameplay and menu actions are separate groups.
5. Tap **Return to game** and release all controls briefly. Returning from settings requires neutral controls to prevent unintended actions.

**Restore defaults** resets bindings. Movement stays on the left stick and D-pad. Default Android names: BUTTON_A jump, BUTTON_X sword, BUTTON_B shoot, BUTTON_Y weapon, BUTTON_START pause. Menu: BUTTON_A confirm, BUTTON_B back. Printed controller labels can differ; bind by pressing the physical button.

Bindings are shared by controllers on this installation, stored in the application's `controller-bindings.txt`, rather than separate per-model profiles. Changing controller mode may require rebinding. Pairing alone does not verify gameplay. If the controller reports two triggers as the same indistinguishable input, the application cannot bind them separately.

Physical controller testing is limited to the modes and actions named in each [test report](validation/GAMEPAD.md). Pairing history above is not a current device allocation. See [the handoff](HANDOFF.md) before operating shared phones.
