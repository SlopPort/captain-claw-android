# Validate imported configuration / Kontrola importowanej konfiguracji

OpenAI Codex (LLM), 2026-10-22. Controller tests excluded.

## Problem and implementation

Previously the importer checked outer archive entries and REZ framing but could publish a malformed `config.xml`. A correct ZIP CRC does not validate the XML inside. Immediately before the existing transaction commit, both ZIP and direct-REZ workflows now validate the staged configuration: maximum 1 MiB, one `Configuration` root, matched/closed element stack, no DTD and no unresolved entity reference. Errors have a PL/EN app-owned prefix and preserve the original exception as their cause. Direct REZ generates its configuration using the APK template and passes the same gate.

The check reads only staging; it does not rewrite the document or touch existing live data. Failure follows existing recovery/cleanup before re-enabling import. This is XML framing validation, not a full engine-settings schema, semantic/range checking of every number or validation of every original game resource. Existing configurations are not silently reset. Full SAF interaction and actual full-disk tests remain open.

## Actual parser failures retained

The first ARM candidate SHA-256 `e7299a6573de1093ae6954d2381f59df09395cd85fef6b6de6791177b6143cee` failed `config-features-huawei-0.4.22.txt`: Android accepted the unclosed `<Configuration>` when EOF was treated as sufficient. Explicit element-stack validation fixed that.

The subsequent ARM candidate `0fb591d61b0c40f9528e91d98ad44fad61596dc2a0b1f431b736e5166f545a2f` and separate x86_64 `d256f7aac8bc265a7ebff33c76b7c56df13dbd63d624ecb6e942004b28840cfe` passed eight cases. Expanded `config-extra-baseline-api21-0.4.22.txt` then failed on an undefined entity: `nextToken()` exposes an unresolved ENTITY_REF without necessarily throwing. That candidate is superseded. The corrected code explicitly rejects a missing entity replacement; predefined entities in the actual generated config remain valid. Failures were not relabeled as success.

## Corrected exact candidates

- ARM64 + ARMv7 SHA-256 `101e023259075dd88a113c6ea45ae9590771e1d6c1274a390ef4f5783af786fd`.
- Separate x86_64 SHA-256 `82a27c60a033d4ee85728d5586b609f651f9d194f0ca924d5433bd3108e9a2e4`.
- Both ARM ABIs, static ARM64 16 KB ELF alignment, zip alignment and APK signature checks passed. These development packages use a debug signing key.

`config-features-huawei-0.4.22-r5.txt` and `config-features-api21-0.4.22-r5.txt`: actual Android 10/5 parsers passed the generated valid document and rejected all eleven cases: empty, unclosed root, wrong root, DTD, duplicate root, wrong closing tag, bad nesting, leading text, trailing text, unresolved entity and >1 MiB input. Existing save, support-font/art and startup/staging fixtures also passed. Tests run in an isolated app-owned folder; they do not perform a real document-picker import or replace the live installation.

## Polski

Instalator sprawdza teraz `config.xml` przed podmianą pięciu plików danych gry. Odrzuca m.in. ucięty XML, błędny korzeń, niedopasowane znaczniki i niezdefiniowaną encję. Jedenaście takich prób przeszło na Huawei i emulatorze Androida 5. Pierwsze dwie nieudane iteracje są zachowane w raportach; wykryły realne ograniczenia parsera Androida. Nie jest to pełna kontrola wszystkich wartości ustawień ani zaliczenie całej obsługi selektora plików.
