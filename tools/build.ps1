param([string]$Abis = 'arm64-v8a')
$ErrorActionPreference = 'Stop'
$portRoot = Split-Path $PSScriptRoot -Parent
if (-not $env:JAVA_HOME) { $env:JAVA_HOME = 'C:/Program Files/Android/Android Studio/jbr' }
if (-not $env:ANDROID_HOME) { $env:ANDROID_HOME = "$env:LOCALAPPDATA/Android/Sdk" }
$gradleExecutable = Join-Path $portRoot 'gradlew.bat'
Push-Location $portRoot
try {
    & $gradleExecutable --no-daemon --console=plain "-Pabis=$Abis" :app:assembleDebug
    if ($LASTEXITCODE -ne 0) { throw "Build failed: $LASTEXITCODE" }
} finally { Pop-Location }
