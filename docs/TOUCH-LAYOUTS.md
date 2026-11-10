# Touch control layouts

Open **Options → Controls**, or use the **PAD** overlay, to choose a touch layout. The selection saves automatically and applies after returning to the game, without restarting. Physical controller bindings remain on the same screen.

- **Classic:** existing stick and action positions.
- **Comfort:** larger jump, melee and shoot buttons.
- **Jump beside attack:** swaps jump and melee positions.
- **Left-handed:** movement on the right, actions on the left.

These are generic arrangements inspired by common modern touch platformer interfaces, not exact presets for named commercial games. They change placement and size, not physics or available actions. Climbing, crouching, variable jump height, weapon switching and simultaneous movement/actions remain available.

The unsupported multiplayer entry is removed from Android menus. Other menu rows retain their coordinates.

Implementation and automated validation: OpenAI Codex (LLM), guided by human requirements. Menu automation does not establish gameplay comfort or a complete campaign playthrough. See the validation report for actual device coverage.

## Movement and button customization

The movement selector offers a fixed stick, a floating stick anchored at the first touch on the movement side, or four directional buttons. Direction buttons support dragging between directions and simultaneous touches. Left-handed layouts also mirror the movement controls.

Stick dead zone ranges from 8 to 28 logical pixels (default 14); smaller values respond to smaller thumb movements. The button editor separately adjusts jump, melee, shoot, weapon and pause: size 60–130%, horizontal/vertical offsets -100 to 100 logical pixels. Each slider saves on release; settings apply after returning to the game. Buttons are clamped to the screen. Users should avoid overlapping controls. Reset in the editor restores only these button adjustments.

## Difficulty

Options → Difficulty offers exactly three presets:

| Preset | Damage received | Healing from pickups |
| --- | --- | --- |
| Easy | 50% | 150% |
| Normal | 100% | 100% |
| Hard | 150% | 50% |

Normal is the default. Positive fractional amounts round upward, so a nonzero effect never becomes zero. Only player damage and healing pickups are scaled. Enemy health, player attack damage, ammunition, lives, movement, checkpoints and lethal terrain rules remain unchanged. Difficulty is stored with app preferences and changes future damage/healing, not current health or saved progress.
