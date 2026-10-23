# Import flow 0.4.26 / Przebieg importu

OpenAI Codex (LLM), 2026-10-23. Physical Redmi Note 8 / Android 16 and Huawei
P9 Lite / Android 10. Exact debug APK (code 38) SHA-256:
`f32e9e96e64b91dd12ea7eff0303a97ea3c7abf1d9b16fbe08f6fa4023a3cb1f`.

## Verified / Potwierdzone

On both devices the production launcher, its async worker and ContentResolver ran
with ordinary target-app permissions, without broad storage grants or adopted
shell identity. The host isolated a missing font to reach first-install UI and
backed up support/config/save files. Four cases passed:

1. Open the actual system document picker from the real button, verify the active
   window belongs to the resolved picker, cancel with accessibility Back, require
   return to this app and an enabled button. No other foreground app receives input.
2. Inject a cancelled picker callback; original config/support/progress unchanged.
3. Supply an invalid 168-byte REZ through a real content URI; production import
   rejects it, re-enables the chooser and preserves config/support/progress.
4. Import the user's full 107,297,326-byte REZ through the content URI and normal
   production validation/staging/commit. Native launch intent follows success.
   Its test monitor blocks native startup so the host can restore files safely.

Cases 2â€“4 inject a picker result into the production Activity callback. They do
**not** prove selecting the full file through DocumentsUI, third-party cloud
providers or every ZIP workflow. The first case alone exercises real picker UI.
The provider is packaged only in the test APK, serves one read-only copied fixture
behind a random per-run capability and has no access to the game's directory.
The host removes that fixture/token afterwards. It never distributes game data.

Final cleanup runs production startup recovery before byte-exact restoration of
support/config/save files and verifies the full REZ hash. Instrumentation calls
have a 180-second host timeout. Private report prefixes:
`import-flow-redmi-0.4.26-final`, `import-flow-huawei-0.4.26-final`.
Huawei PL/EN/footer and parser/save/support checks also passed on this exact APK.
All six native libraries are byte-identical to 0.4.25 debug; only launcher UI and
version metadata changed. This does not transfer evidence to the release variant.

The importer now scrolls so its controls can be revealed on small screens without
changing the system font. Earlier save-tool scrolling remains in place.

## Retained failed setup

The first Redmi attempt used an IntentFilter ActivityMonitor. It also matched an
actionless launcher start, leaving startActivitySync blocked before import. The
own-app process was stopped, host cleanup restored original bytes, and the failure
is retained under `import-flow-redmi-0.4.26`. The test now injects only the callback;
the separate real-picker cancellation path does not intercept its launch.
Intermediate r2/r3 successes are retained separately, not substituted for this
failed setup. No production import crash was established by that failure.

## Polski

Na obu telefonach przeszĹ‚o otwarcie i anulowanie prawdziwego selektora, odrzucenie
bĹ‚Ä™dnego REZ i import peĹ‚nego pliku uĹĽytkownika. WybĂłr pliku dla peĹ‚nego importu
byĹ‚ zastÄ…piony kontrolowanÄ… odpowiedziÄ…; samo kopiowanie, walidacja i transakcja
wykonaĹ‚y siÄ™ w prawdziwym kodzie aplikacji, z jej zwykĹ‚ymi uprawnieniami.
WĹ‚asne dane i zapisy przywrĂłcono i porĂłwnano. Plik gry nie trafia do repozytorium.
Nadal potrzebne sÄ… prĂłby wybierania duĹĽego pliku w samym selektorze, ZIP i dostawcy
chmurowi. Nie zastÄ™pujemy ich wynikami tej ograniczonej prĂłby.

## Full ZIP and adversarial archives / PeĹ‚ny ZIP i bĹ‚Ä™dne paczki

Six further cases passed on each physical phone, same exact debug APK above:
`import-zip-redmi-0.4.26` and `import-zip-huawei-0.4.26`.

- Full prepared ZIP containing the full user REZ and four support files committed
  successfully and requested native startup; no progress replacement.
- `../SAVES.XML` entry was rejected without writing outside staging.
- Duplicate config.xml entries, a missing required-file set, a CRC-corrupted
  entry and malformed config in a full-size ZIP were rejected.
- Each case resets support/config fixtures; production recovery runs before final
  restoration. Original REZ, support, config and save bytes verified unchanged.
- A separate immutable provider-side REZ copy is retained until restoration is
  verified, so a ZIP fixture can never accidentally become the recovery source.

These six cases inject only the picker result; extraction/validation/commit are
production code under ordinary app permissions. They do not add a claim of full
file selection through DocumentsUI. ZIP test copies/logs remain private, ignored
reports containing the user's own data; do not publish them.

Na obu telefonach przeszedĹ‚ peĹ‚ny ZIP. Odrzucono prĂłbÄ™ wyjĹ›cia Ĺ›cieĹĽkÄ… poza katalog,
duplikaty, brak plikĂłw, bĹ‚Ä™dne CRC i uszkodzony XML w duĹĽej paczce. Weryfikowano
niezmieniony zapis i dane; kaĹĽda prĂłba ma wĹ‚asny raport. Archiwa testowe zawierajÄ…
wĹ‚asne dane uĹĽytkownika i pozostajÄ… poza repozytorium.

## Retained real-file selection failures and later Redmi pass

An additional real DocumentsUI REZ-selection experiment did not pass. Redmi
`import-picker-redmi-0.4.26` could not find the freshly copied fixture. Retry r2
was stopped while stalled; r3 reached the 180-second host timeout. Host production
recovery and original-file restoration completed, and temporary provider/public
Download copies were removed. A read-only screenshot showed the picker at the
storage-root directory; the exact automation failure remains unconfirmed.

Experimental source and private screenshots are retained under ignored reports;
the public default test remains the passing cancellation/callback/stream/ZIP
suite. No full interactive REZ-selection pass is claimed. This does not establish
a production import crash: the production full-REZ stream and ZIP cases passed.

Dodatkowa automatyzacja wyboru pliku w samym selektorze nie przeszĹ‚a. Zachowano
nieudane prĂłby i eksperymentalny kod, ale nie zaliczono ich do sukcesĂłw. PrzywrĂłcono
pliki i usuniÄ™to wyĹ‚Ä…cznie jednorazowe kopie testowe. Ten punkt pozostaje otwarty.

The later Redmi r6 attempt **passed** actual selection of the full REZ through
DocumentsUI, production callback, URI grant and import worker, with original bytes
restored. It uses a test-only initial Download URI and a unique temporary file;
the ordinary production choose-button launch is independently covered by the
real cancellation trial. Temporary Download/provider files were removed.

Failed r4/r5 attempts are retained too. Diagnosis found an orphan picker task after
intentional force-stop, and navigation assumptions about list depth/type. Fresh
fixture launches now use NEW_TASK|CLEAR_TOP; scrolling addresses the actual
`dir_list` rather than toolbar/chip containers. No production game code was changed
for these test fixes. The raw r6 global `picker_result_injected` metadata remains
true from the older helper; its case field correctly says false. The helper now
computes the global field from its cases. Do not overwrite the raw evidence.
Huawei r4 also passed full interactive selection with ordinary app permissions; earlier failed attempts remain retained. Android 10 exposed a file title without a working accessibility click, so the test used UiAutomation touchscreen input on that exact visible title, only after checking the foreground DocumentsUI package. No other application received input.

Po kolejnych poprawkach samego testu peĹ‚ny wybĂłr REZ w selektorze Redmi przeszedĹ‚.
Nie usuniÄ™to wczeĹ›niejszych niepowodzeĹ„. Nie przenosimy wyniku automatycznie na
Huawei ani inne selektory plikĂłw.
