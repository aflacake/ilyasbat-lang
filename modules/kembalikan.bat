@echo off
REM modules/kembalikan.bat

if "%1"=="kembalikan" (
    setlocal enabledelayedexpansion

    for /f "delims=" %%A in ('python helpers\kembalikan.py "%2"') do (
        set "result=%%A"
    )

    endlocal & set "hasil=%result%"
)
