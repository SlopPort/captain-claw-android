# OpenAI Codex: compile against the actual patched, pinned Box2D sources.
# Requires a host g++ (for example MSYS2 UCRT64); not needed to install the game.
$ErrorActionPreference = 'Stop'
$portRoot = Split-Path -Parent $PSScriptRoot
$previousTaskPath = $env:PATH
Push-Location -LiteralPath $portRoot
try {
    $compiler = (Get-Command g++ -ErrorAction Stop).Source
    # MSYS2 executables need their adjacent runtime DLLs on PATH as well.
    $env:PATH = (Split-Path -Parent $compiler) + ';' + $env:PATH
    New-Item -ItemType Directory -Force -Path build | Out-Null
    $sources = Get-ChildItem -LiteralPath upstream/OpenClaw/Box2D/Box2D -Recurse -Filter *.cpp |
        ForEach-Object FullName
    & $compiler -std=c++11 -O2 -I upstream/OpenClaw/Box2D tests/box2d_pair_filter_test.cpp @sources -o build/box2d_pair_filter_test.exe
    if ($LASTEXITCODE -ne 0) { throw 'Box2D test compilation failed' }
    & ./build/box2d_pair_filter_test.exe
    if ($LASTEXITCODE -ne 0) { throw 'Box2D equivalence test failed' }
} finally {
    $env:PATH = $previousTaskPath
    Pop-Location
}
