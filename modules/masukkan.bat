REM modules/masukkan.bat

@echo off

if "%1"=="masukkan" (
    setlocal enabledelayedexpansion

    set "varname=%2"

    for /f "delims=" %%A in ('python helpers\masukkan.py') do (
        set "result=%%A"
    )

    endlocal & set "%varname%=%result%"
)
