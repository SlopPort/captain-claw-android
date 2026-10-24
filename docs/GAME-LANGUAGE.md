# Game-data language

Research by OpenAI Codex (LLM), 2026-10-23.

The port already offers Polish and English interface text. Select the language
before importing data, or in **PAD → Language**, then restart the game for native
menus. This does not translate recorded voices or replace imported game data.

Claw and enemies have recorded speech. A Polish data installation cannot produce
the original English performances merely by selecting English in settings.
The original graphics and any movies are also separate from our interface text.

The [Claw Recluse downloads page](https://captainclaw.net/en/downloads.html)
lists full game packages, a sounds/quotes reference and cutscenes. The
[Polish page](https://captainclaw.net/download.html) identifies English cutscenes.
Searches did not establish a standalone English voice pack or permission to
redistribute English commercial recordings with this open-source port. Availability
on a fan site is not evidence of a redistribution licence. No such files were
downloaded or added to the repository for this investigation.

Further research found a historical sound-pack announcement dated 2005-12-10 in
the [site archive](https://captainclaw.net/en/archive.html), described by its
compiler as containing all game sounds. A 2006-09-16 entry says large downloads
including that pack were removed. The old soundpack.zip host failed DNS resolution
during a HEAD-only check on 2026-10-23; current availability, language, completeness
and reuse permission are therefore unverified. This is a lead, not an installable
language-pack recommendation. The human confirmed having only Polish game data.

For English recordings, the supported data-import route is to supply the full
CLAW.REZ from your own legitimately obtained English installation, or prepare a
game-data.zip from that installation using this project's packer. English voice
playback with such a data set has **not yet been verified** in this investigation.
Windows patches and CLAW.FEC cutscene files are not Android language packs;
the port's staged finale does not establish original movie playback support.

At present only one imported game-data set is active. Switching PL/EN changes
the interface, not between two installed dubbing sets. A future dubbing selector
needs separately supplied user-owned data, validated imports, interruption-safe
switching, unchanged saves and settings, and playback checks for Claw, enemies
and bosses. Do not advertise that feature as implemented or all dialogue as English.
