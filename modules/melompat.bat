REM modules/melompat.bat

@echo off

if "%1"=="melompat" (
    setlocal enabledelayedexpansion

    for /f "delims=" %%A in ('python helpers\melompat.py "%2"') do (
        set "target=%%A"
    )

    endlocal & set "next_label=%target%"
)
