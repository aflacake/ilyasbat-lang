@echo off
REM main.bat

setlocal EnableDelayedExpansion

if exist ".env.bat" call ".env.bat"

if "%~1"=="" (
    echo Tidak ada file .ibat yang diberikan.
    echo Contoh: main.bat skrip.ibat
    exit /b 1
)

set "source_file=%~1"
set "module_dir=modules"

if not exist "%source_file%" (
    echo File "%source_file%" tidak ditemukan.
    exit /b 1
)

for /f "usebackq delims=" %%A in ("%source_file%") do (
    set "line=%%A"

    for /f "tokens=1*" %%B in ("!line!") do (
        set "cmd=%%B"
        set "args=%%C"
    )

    if exist "%module_dir%\!cmd!.bat" (
        set "output="
        for /f "usebackq delims=" %%O in (`call "%module_dir%\!cmd!.bat" !args!`) do (
            set "output=%%O"
        )

        if errorlevel 1 (
            echo Terjadi kesalahan saat menjalankan !cmd!
            exit /b 1
        )

        if defined output (
            echo !output!
            set "hasil=!output!"
        )

    ) else (
        echo Perintah '!cmd!' tidak dikenal
        exit /b 1
    )

    REM melompat
    if defined next_label (
        goto !next_label!
    )
)
