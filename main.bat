@echo off
REM main.bat

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
        REM Jalankan modul dan tangkap output ke variabel
        for /f "usebackq delims=" %%O in (`call "%module_dir%\!cmd!.bat" !args!`) do (
            set "output=%%O"
        )

        REM Tangani errorlevel
        if errorlevel 1 (
            echo Terjadi kesalahan saat menjalankan !cmd!
            exit /b 1
        )

        REM Tampilkan keluaran
        if defined output (
            echo !output!
            set "keluaran="
        )

    ) else (
        echo Perintah !cmd! tidak dikenal
        exit /b 1
    )

    REM melompat
    if defined next_label (
        goto %next_label%
    )
)

endlocal
