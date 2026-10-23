# Readiness checks / Kontrole przed wydaniem

OpenAI Codex (LLM), 2026-10-23. Human owns natural campaign playtesting.
Ask before using Redmi. No physical-controller testing in this batch.

## English

`gradlew :app:lintDebug` completed successfully on the current 0.4.24-dev sources:
**0 errors, 33 warnings**. This is static analysis, not a runtime compatibility
certificate. No phone installation or production-code change was needed.
Ignored local reports: `reports/lint-release-readiness-0.4.24.txt` and
`app/build/reports/lint-results-debug.{txt,xml,html}`.

Warning groups: ObsoleteSdkInt 12, StaticFieldLeak 5, InlinedApi 4, SetTextI18n 3,
UnusedResources 2, and one each of ApplySharedPref, DefaultLocale,
AppBundleLocaleChanges, DiscouragedApi, ChromeOsAbiSupport, DataExtractionRules,
MissingApplicationIcon. No new lint suppressions or baselines were added.

The five static-context warnings belong to SDL and still require lifecycle-aware
review; a warning alone is not a measured leak. The four inlined-axis warnings
are in SDL's API24 relative-mouse class; review API-based listener selection before
changing it. Controller transport tests remain deferred. App-owned follow-ups:
provide an original/non-commercial app icon, review Android-12+ backup/transfer
rules, text formatting and unused messages. Landscape/tablet behavior still needs
runtime checks. The locale warning concerns potential language splitting in an
App Bundle; currently distributed APKs are not evidence for a future AAB workflow.
ChromeOS/x86 release support is not established by separate emulator builds.

[Actual ENOSPC checks](IMPORT-FULL-DISK.md) passed for backup and rollback on a
bounded API-21 emulator filesystem. The existing 64 host transaction checks also
passed. Still open: full SAF picker/cancellation workflow, large real data imports,
ordinary app-UID full-storage behavior, final APK runtime matrix, sustained Huawei
performance, touch/lifecycle regressions and signed release preparation. No claim
that the whole installation or Android-compatibility gate is closed.

## Polski

Analiza Android Lint przeszła: **0 błędów i 33 ostrzeżenia**, bez wyciszania
ostrzeżeń. To nie dowód działania na wszystkich Androidach. Ostrzeżenia obejmują
kod SDL oraz nasze sprawy do dopracowania: ikonę aplikacji, zasady kopii/przenoszenia
danych w nowszych Androidach, formatowanie napisów i nieużywane komunikaty.
Nie uznajemy ostrzeżeń o wyciekach za zmierzony wyciek pamięci.

Rzeczywisty brak miejsca sprawdzono dla transakcji importu, lecz cały scenariusz
instalacji przez selektor plików pozostaje otwarty. Pozostałe punkty nadal obejmują
duże dane, końcowe testy APK na Androidach, dłuższe pomiary Huawei, dotyk i cykl życia
aplikacji oraz podpisanie wydania. Nie instalowano nic na telefonach. Kampanię
testuje użytkownik; przed jakimkolwiek użyciem Redmi trzeba zapytać o dostępność.
