# Release signing / Podpis wydania

Prepared by OpenAI Codex (LLM), 2026-10-23. Source authorship and game-data rights
remain as described in NOTICE. A signed development candidate is not release 1.0.

## Co to znaczy dla właściciela projektu?

Android wymaga podpisu APK. Podpis pozwala mu sprawdzić, czy aktualizacja pochodzi
od posiadacza tego samego klucza co zainstalowana aplikacja. To nie jest klucz do
GitHuba, konto Google, licencja gry ani zabezpieczenie kodu przed kopiowaniem.
Otwarte źródła pozostają otwarte; każdy może zbudować i podpisać własny wariant.

Lokalnie utworzono dwa pliki: `private-signing/pazur-release.keystore` zawiera
prywatny klucz podpisujący, a `private-signing/password.txt` zawiera jego hasło.
Nie trzeba ich wysyłać ani podawać hasła w rozmowie. Zachowaj kopię obu w prywatnym,
bezpiecznym miejscu poza projektem, najlepiej jako zaszyfrowaną kopię zapasową.
Nie umieszczaj ich w repozytorium — także prywatnym. Publiczny certyfikat i jego
odcisk mogą być jawne; prywatny klucz i hasło nie.

Oba telefony nadal używają podpisu testowego debug. Nowy klucz wykorzystano tylko
do kandydata i osobnego testu; nie zastąpiono nim Twojej instalacji. Na razie nic
nie musisz odinstalowywać ani zmieniać na telefonie. Publikacja samych źródeł nie
wymaga udostępniania żadnego z tych plików.

## Plain-English explanation

Android uses an APK signature to accept updates from the same signing identity.
This is unrelated to GitHub login, Google accounts or ownership of the original
game. Open source does not require publishing the private signing key: other
people can build and sign their own variants. The local keystore contains the
private key; password.txt contains its password. Privately back up both outside
the checkout, preferably encrypted. Do not upload either file or share its contents.
The phones still use debug signing; no uninstall or migration is needed now.

## English

A first release identity was generated locally with subject `CN=SlopPort`, RSA
3072, PKCS12. Its files are **private**:

- `private-signing/pazur-release.keystore`
- `private-signing/password.txt`

Back up **both** outside this checkout in private storage before distributing a
release. Losing the key prevents future updates with the same identity. These
files must never be uploaded to GitHub, attached to an issue or included in a
source ZIP. The directory is ignored and both source/history checks reject it.
No human name is present in the certificate. The password is generated locally,
read from a file and never passed directly on the command line.

To create an identity in a fresh checkout, only if none already exists:

```powershell
python tools/create_release_key.py --keytool "C:/Program Files/Android/Android Studio/jbr/bin/keytool.exe"
```

The tool refuses an existing directory. Never regenerate the key for each version.

Build with the pinned SDK/NDK from the build guide and these local environment
variables (paths only, not passwords):

```powershell
$env:PAZUR_RELEASE_KEYSTORE = (Join-Path $PWD 'private-signing/pazur-release.keystore')
$env:PAZUR_RELEASE_PASSWORD_FILE = (Join-Path $PWD 'private-signing/password.txt')
./gradlew.bat '-Pabis=arm64-v8a,armeabi-v7a' :app:assembleRelease
```

Release builds fail if signing files are absent. Debug builds do not require them.
The result is `app/build/outputs/apk/release/app-release.apk`. Verify its signature,
16 KB alignment and both ABIs as described in BUILDING.en.md. Keep matching source
and SHA-256 checksums. Never assume debug-package tests certify a release package:
its signature, manifest and native build variant differ and need their own evidence.

**Existing test installations use the SDK debug certificate. Android will reject
an in-place update signed with the new release identity.** Neither phone was
uninstalled or migrated for signing preparation. Keep the debug test channel for
now. Before an eventual migration, export progress using Save backups, separately
retain the original REZ/ZIP, and verify the exported save. Only then explicitly
plan removal/reinstallation and restore the save. Uninstalling removes app-private
files; a signature failure is not a reason to uninstall without a verified backup.
Do not distribute an unsigned APK or publish the test companion as the game.

## Polski

Przygotowano lokalny klucz wydania bez imienia człowieka: `CN=SlopPort`, RSA 3072.
Plik klucza i plik hasła znajdują się w prywatnym katalogu `private-signing/`.
**Zachowaj prywatną kopię obu plików poza katalogiem projektu przed dystrybucją.**
Nie wrzucaj ich na GitHub ani do zgłoszeń. Utrata klucza uniemożliwia podpisanie
kolejnej aktualizacji tą samą tożsamością. Nie generuj nowego klucza co wydanie.

Polecenie powyżej tworzy klucz tylko wtedy, gdy katalog jeszcze nie istnieje.
Zmienne środowiskowe wskazują pliki; hasła nie wpisuje się do polecenia ani źródeł.
Kompilacja release bez klucza jest blokowana, a debug działa jak wcześniej.

Obecne instalacje na telefonach mają podpis testowy SDK. Nowy podpis nie pozwoli
nadpisać ich aktualizacją. Nie odinstalowano gry z żadnego telefonu. Przed przyszłą
zmianą kanału trzeba wyeksportować i sprawdzić zapis, zachować własne dane gry,
a dopiero potem świadomie przeprowadzić reinstalację i przywrócenie postępu.
Podpisany kandydat nadal wymaga własnych prób; nie nazywamy go wersją 1.0.

[0.4.26 candidate verification and isolated runtime scope](validation/RELEASE-0.4.26.md).

[0.4.27 candidate verification and isolated controls](validation/RELEASE-0.4.27.md).
