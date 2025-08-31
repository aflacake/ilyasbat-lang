@echo off
REM modules/menyimpan.bat

if "%1"=="menyimpan" (
    setlocal enabledelayedexpansion

    set "key=%2"
    set "value=%3"

    python helpers\menyimpan.py "!key!" "!value!"

    endlocal
)
