@echo off
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
    py -3 tools\prepare_game_data_gui.py
) else (
    python tools\prepare_game_data_gui.py
)
if errorlevel 1 (
    echo.
    echo Install Python 3.11+ with Tcl/Tk and Git, then try again.
    echo Zainstaluj Python 3.11+ z Tcl/Tk oraz Git i sprobuj ponownie.
    pause
)
