# Tile query and conversion audit — 2026-11-12

OpenAI Codex (LLM) performed this static audit. The human remains anonymous. This is a bounded finding within the [full audit](REA-FULL-AUDIT.md), not a completed engine reconstruction.

## Exact scope and original evidence

Target: supplied CLAW.EXE, SHA-256 `33cf6e2663823f073d769c3d05a1ad5e13e3e4993ad2cb6822617737395004c6`. This modified distribution is not certified as a pristine retail executable. Raw commercial bytes and instruction records remain private.

REA's bounded read of the tile vtables at `0x51414c`, `0x51418c` and `0x5141cc` joins their query slot `+0x18` to `0x4ce9e0`, `0x4cea30` and `0x4ceb10`. Evidence: `ev_b853aa2a827fb35ff7895edb33e38cef948b5b32d8cc45ce205bafec072ff8b9`. Supplied CrazyHook constants were naming hints; the pointers and methods were checked independently through REA.

- The first method returns its configured attribute independently of the coordinates.
- The second compares X and Y against an **inclusive** rectangle: both right and bottom belong to the inside region. It returns the configured inside or outside attribute. Entry evidence: `ev_94f45b59fd45eea53f08742bcd9f6deacc09e24857f882475284d233c394b663`.
- The third reads a byte from a row-addressed mask, using a configured shift and base pointer. It has no local bounds check; valid coordinates, storage and configuration remain caller/setup obligations.

Point-query routine `0x421ad0` clamps map coordinates, handles sentinel tile entries and dispatches the tile-local query. Evidence: `ev_c5ffa759ef183dccd50ee851bc0f4c89c5f54282da1d3a596006f8da72756588`.

The object initializer `0x4c7540` sets terrain sampling fields `+0xf8` and `+0xfc` to **10**. Evidence: `ev_534f2436e15c8638296980bec04822c15475e1f9a931382e15bb3a7aa83a48c9`. This closes the default value for that initialization path; it does not prove every subsequent mutation or sampling endpoint. Identical offsets in player auxiliary data and motion-state structures are different fields.

### Additional double-tile boundary queries

Two further unowned methods were decoded through REA rather than assumed absent because Ghidra did not enumerate them. Both use four stack arguments and signed comparisons. Names below describe the observed contract, not recovered original symbols.

- Vtable slot `+0x20`, `0x4d7500`: when Y lies within inclusive top/bottom and X is at least left, a point to the right of the inside region yields the right bound and inside attribute through two output pointers. A point at/between left and right yields `left - 1` and the outside attribute only when left is positive. Otherwise it returns false without writing either output. Successful branches return 1. Entry evidence: `ev_1ac28ff01b5d26adafe1b128a94df4822ae25c9ffe18db219660e052f1b972e5`.
- Slot `+0x24`, `0x4d7560`, applies the same coordinate branches but additionally requires the selected region's attribute to equal the third argument. It writes only the selected bound through the fourth argument when successful. Entry evidence: `ev_a028bc3a09aa37e7d0fc000480610dbb9a30ff33749bf670bf0d7ebceb05bd89`.

These bounded methods reinforce the distinction between an inclusive right bound and the last outside cell `left - 1`. The [subsequent boundary-family review](REA-TILE-BOUNDARIES-2026-11-12.md) joins all eight double-tile directional entries; callers and output-pointer validity remain open. They must not be described as a new hero movement rule: the four terrain edge consumers already inspected call point-query slot `+0x18`, not these two slots. The port uses Box2D fixtures instead of a direct implementation of these virtual query contracts.

## Reproducible converter comparison

The [host harness](../../tests/tile_partition_audit.cpp) compiles the actual current `ParseCollisionRectanglesFromTile` and `IsInBetween` definitions extracted from OpenClaw's `Engine/Util/Util.cpp`. Its independent reference predicate follows the observed inclusive comparisons. It uses synthetic 64×64 descriptions with solid inside and clear outside; no original resources are required.

Run from the repository root with a host C++ compiler available:

```text
python tools/audit_tile_partition.py --report tile-partition-new-run
```

Each report name must be new. Exit **1 means a recorded discrepancy**, not a passed parity check. The script retains build diagnostics, results and input hashes under ignored `reports/`. The first local compiler setup failed before producing a comparison; it remains separate from the successful second run. The second run used MSYS2 UCRT64 g++ 15.1.0 with its directory prepended only to the child process PATH.

| Synthetic description | Differing pixel cells | Pieces extending outside tile |
| --- | ---: | ---: |
| Single attribute | 0 | 0 |
| Top half | 64 | 1 |
| Right half | 0 | 0 |
| Bottom half | 0 | 0 |
| Left half | 64 | 1 |
| Middle horizontal band | 2,112 | 0 |
| Middle vertical stripe | 64 | 0 |

Source SHA-256: `ef64fb727908220f2155cac6799ed941dabcf48ea8bea4de1ecd7c859ec575dd`. Harness SHA-256: `cc18a4d7e11c3f2a5e59a5cef19087e054bc5179c97c482c6afc60b2583dd810`.

The top/left branches omit an inclusive row/column from solid geometry and extend the clear piece past the tile. The middle horizontal band also starts its solid piece at Y=0 rather than the configured top. Other branches require a complete case/data audit; these seven examples do not certify the entire converter.

## Impact and remaining work

### Descriptor loading and mask boundary

The original factory `0x4cc390` accepts type 1, 2 or 3, allocates different object sizes and installs the corresponding observed vtable. It invokes initialization slot `+0x0c`; a false initialization result triggers deletion and a null return. A null descriptor and unknown type also return null. The allocation-null path reaches a dereference, but the previously joined default allocation handler throws: retain this as configuration-dependent behavior, not a demonstrated ordinary allocation crash. The factory's actual upstream caller remains unjoined. Evidence: `ev_d29ce4f8c8db8529cc16472bf4459dadbdb442cc2997adbe43ef2c53224f0b17`.

Initializer `0x4d7100` copies the single descriptor's dimensions and attribute. `0x4d74b0` copies the double descriptor's dimensions, two attributes and four rectangle bounds **without an inclusive-to-exclusive adjustment**. These copies connect the query fields to descriptor storage. Evidence: `ev_960e6afcf1e6692e39d9d1d6db2addd8cb1f4e2e65214ae27f288f52dc0f628c`, `ev_fcafc504d3ea9c642568679476bb8d8bb6af32ea9963581c4e4f590858024114`.

Mask initializer `0x4d7130` multiplies two dimensions to obtain its allocation/copy size. It derives a shift by repeatedly halving the second dimension, then requires the first dimension to equal `1 << shift`. It copies mask bytes from the descriptor after its dimensions. Do not simplify this into a proved generic square/power-of-two constraint: the assembly checks this specific relationship. Bounds, multiplication overflow, descriptor storage validity and all setup callers remain open. Destructor `0x4ceab0` releases a non-null mask buffer, clears it and installs the base vtable. Evidence: `ev_e7efebab9f96f8f33f4a27b401a71ee4e5a4703e480c89333e10872ba963592a`, `ev_68fe8dddf12759b79a2cabca72ee51952a4b76eda39f4c98f6501b74536ef81e`.

In the port, `libwap/WwdFile.cpp::ReadTileDescriptions` treats every non-single type as a double rectangle; `Engine/Util/Converters.cpp` does the same when producing XML. Consequently, original mask support is not established by these paths. This is a format-compatibility gap, not proof that a stock campaign level currently fails.

### Supplied local dataset survey

The [read-only survey](../../tools/audit_tile_descriptions.py) follows the checked libwap header offsets and tile-descriptor layout, validates decompression length and stops on unknown descriptor types rather than guessing. A successful run over the supplied local `Assets/LEVEL1` through `LEVEL14` found **9,336 descriptions: 8,231 single and 1,105 double; no type 3**. Input hashes and descriptor records remain private in `reports/rea-tile-descriptions-2026-11-12/`. These files are not independently certified retail data or the currently installed phone dataset.

```text
python tools/audit_tile_descriptions.py --assets PATH_TO_YOUR_ASSETS --report tile-descriptions-new-run
```

Level 1 contains left-half-shaped descriptions, but their inside/outside categories differ from the synthetic solid-inside/clear-outside control. A matching rectangle shape alone does not prove the same effective solid error. Tile placement, all real category combinations and runtime consumers remain to be joined; no natural level-1/2 snag is closed by this survey.

`BaseGameLogic::CreateSinglePhysicsTile` forwards rectangle origins and sizes to `ClawPhysics::VAddStaticGeometry`, which constructs Box2D half-extents without an inclusive-bound correction. Clear pieces produce no solid fixture. The harness therefore establishes a converter-level discrepancy for these inputs.

It does **not** execute Box2D, model collision skin/contact resolution, prove that a particular installed level uses these descriptions, or reproduce the reported level-2 snag. No production collision change, APK installation or device test was performed.

Before a gameplay fix: identify affected descriptions in the user's supplied data, audit all partition branches and attribute combinations, check merged fixtures and support contacts, and retain passing right/bottom controls. Then reproduce the natural location with the human tester. The full machine-code audit remains open, including mask allocation/loading, other tile methods, runtime stride mutations and dependent collision state transitions.
