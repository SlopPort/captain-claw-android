# Publication / Publikacja

## English

Destination: public `SlopPort/captain-claw-android`. This is the Captain Claw
Android adaptation only; another project's concurrent publication must use its
own repository and local checkout. Do not change global credentials, global Git
identity, another project's remote, or force-push shared history.

The adaptation source is GPL-3.0, with dependency-specific licenses retained in
`NOTICE.md`, `licenses/` and packaged license notices. This is not a license for
the commercial Claw game. Do not assume copyright expiry. Do not publish CLAW.REZ,
extracted game resources, maps, music, speech, videos or game-data.zip. OpenClaw
and other upstream authors retain attribution. Adaptation work so far is explicitly
credited to OpenAI Codex (LLM), with human requirements and feedback.

Before the first push:

1. `python tools/check_repository.py` checks tracked/staged source files.
2. `python tools/check_public_history.py` scans reachable historical blobs and
   changed paths, including removed files. Optionally supply a local ignored
   `--private-pattern-file` containing identifiers that must not be published.
   Never commit this pattern file. This heuristic does not replace reviewing art,
   licenses, binary provenance and intended public content.
3. Review `git diff --cached`, `git status`, authors and the exact remote. Raw
   reports, screenshots, player saves, signing keys and credentials stay local.
4. Authenticate the intended account through the normal Git/browser login flow.
   A browser login is not automatically a Git login. Never paste tokens into an
   issue, commit, remote URL, script or chat. Do not reuse another account by accident.
5. Create an empty public repository and push the reviewed main branch normally.
   If the destination already contains unrelated work, stop and choose a new name.

Keep APK releases separate from source publication. The current APK is a debug
signed development build; do not label it a final 1.0 or silently change its signing
key for existing users. Any later binary release must identify its exact source
revision, checksums, source availability, license notices, validation and limitations.
No commercial game-data bundle is a release asset.

Current publication audit: the initial local reachable-history scan inspected
596 blobs (5,679,023 bytes), found none of its excluded paths/credential/private
identifier patterns, and showed adaptation commits authored as Codex. This is a
bounded scan result, not a comprehensive legal or security guarantee. Rerun after
the publication-preparation commit. Do not put a person's real name in project
credits or commit identity without their request; upstream attribution is preserved.

## Polski

Docelowe repozytorium publiczne: `SlopPort/captain-claw-android`. Inny projekt
publikowany równocześnie musi mieć własne repozytorium i katalog roboczy.
Nie zmieniaj globalnego konta Git, cudzych adresów zdalnych ani wspólnej historii
przez wymuszone wysyłanie.

Kod adaptacji jest na GPL-3.0; zachowujemy licencje bibliotek i autorów wskazanych
w NOTICE. To nie daje praw do publikacji danych komercyjnej gry. Nie zakładamy
wygaśnięcia praw autorskich. Poza repozytorium i wydaniami pozostają archiwa gry,
mapy, grafiki, dźwięki, muzyka, filmy, game-data.zip, prywatne raporty, zapisy,
numery urządzeń, klucze podpisu i poświadczenia. Praca nad adaptacją jest jawnie
opisana jako wykonana przez OpenAI Codex (LLM), z wymaganiami i uwagami człowieka.

Przed publikacją uruchom kontrole źródeł i całej historii wymienione wyżej,
przejrzyj przygotowane zmiany oraz dokładny adres repozytorium. Prywatne wzorce
do skanera trzymaj wyłącznie lokalnie. Kontrola wzorców nie zastępuje sprawdzenia
pochodzenia obrazów i licencji. Pierwszy audyt objął 596 obiektów i nie wykazał
sprawdzanych problemów; po ostatnim commicie trzeba go powtórzyć.

Zalogowanie w przeglądarce nie oznacza zalogowania Git. Używaj właściwego konta,
nie wklejaj tokenów do czatu ani plików i nie wylogowuj drugiego projektu.
Publikuj zwykłym wysłaniem sprawdzonej gałęzi do pustego repozytorium. Jeśli nazwa
jest zajęta przez inny projekt, wybierz inną, zamiast nadpisywać zawartość.

Publikacja kodu nie jest deklaracją gotowej gry 1.0. Obecny APK ma podpis testowy;
przyszłe wydanie binarne wymaga wskazania źródeł, sum, licencji i ograniczeń testów.
Danych oryginalnej gry nie dołączamy również do wydań APK.

Scanner validation / Sprawdzenie skanera: four isolated host Git fixtures passed
(clean history, deleted data file retained in history, deleted dummy credential
retained in history, private identifier pattern). Fixture credentials were fake;
no actual game archive or real token was added. Raw fixture reports remain local.
