REM modules/mengembalikan.bat

@echo off

if "%1"=="mengembalikan" (
    setlocal enabledelayedexpansion

    set "key=%2"

    for /f "delims=" %%A in ('python helpers\mengembalikan.py "!key!"') do (
        set "result=%%A"
    )

    endlocal & set "hasil=%result%"
)
