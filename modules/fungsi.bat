@echo off
REM modules/fungsi.bat

setlocal enabledelayedexpansion

set "first=%1"
set "second=%2"

REM -----------------------------
REM DEFINISI FUNGSI
REM -----------------------------
if /i "!first!"=="fungsi" (
    set "func_name=%second%"
    shift
    shift

    REM Ambil semua parameter
    set "params="
    :getparams
    if not "%1"=="" (
        set "params=!params! %1"
        shift
        goto :getparams
    )

    echo [DEF] Fungsi: !func_name! Params:!params!
    echo Ketik isi fungsi. Akhiri dengan "selesai"

    call :captureFunction | python helpers\fungsi.py tulis !func_name! !params!
    endlocal & exit /b 0
)

REM -----------------------------
REM PEMANGGILAN FUNGSI
REM -----------------------------
set "func_name=%first%"
shift

REM Tangkap semua argumen
set "args="
:collectArgs
if not "%1"=="" (
    set "args=!args! %1"
    shift
    goto :collectArgs
)

REM Dapatkan isi fungsi dari Python
for /f "delims=" %%x in ('python helpers\fungsi.py panggil !func_name! !args! 2^>nul') do (
    call main.bat %%x
)

if errorlevel 1 (
    echo Terjadi kesalahan saat memanggil fungsi !func_name!
    endlocal & exit /b 1
)

endlocal
exit /b 0

:captureFunction
set "line="
:inputLoop
set /p "line=> "
echo %line%
if /i "%line%"=="selesai" goto :eof
goto inputLoop
