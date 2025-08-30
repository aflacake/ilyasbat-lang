@echo off
setlocal enabledelayedexpansion

set "source_file=program.ibat"
set "module_dir=modules"

if not exist "!source_file!" (
    echo File !source_file! tidak ditemukan.
    exit /b
)

for /f "usebackq delims=" %%A in ("!source_file!") do (
    call :interpret "%%A"
)

goto :eof

:interpret
set "line=%~1"
for /f "tokens=1*" %%C in (%line%) do (
    set "cmd=%%C"
    set "args=%%D"
)

if exist "%module_dir%\!cmd!.bat" (
    call "%module_dir%\!cmd!.bat" !args!
) else (
    echo Perintah '!cmd!' tidak dikenali.
)
goto :eof
