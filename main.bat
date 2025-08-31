REM main.bat

@echo off
setlocal enabledelayedexpansion

set "source_file=program.ibat"
set "module_dir=modules"

for /f "usebackq delims=" %%A in ("%source_file%") do (
    set "line=%%A"
    for /f "tokens=1*" %%B in ("!line!") do (
        set "cmd=%%B"
        set "args=%%C"
    )

    if exist "%module_dir%\!cmd!.bat" (
        call "%module_dir%\!cmd!.bat" !args!
    ) else (
        echo Perintah !cmd! tidak dikenal
    )
)

endlocal
