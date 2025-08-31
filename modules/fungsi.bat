@echo off
REM modules/fungsi.bat

setlocal enabledelayedexpansion

REM ---------------------------
REM DETEKSI MODE DEFINISI
REM ---------------------------
if /i "%1"=="fungsi" (
    set "func_name=%2"
    shift
    shift

    set "params="
    :getparams
    if not "%1"=="" (
        set "params=!params! %1"
        shift
        goto :getparams
    )

    echo [DEF] Fungsi: !func_name! Params:!params!
    call :captureFunction | python helpers\fungsi.py tulis !func_name! !params!
    endlocal & exit /b 0
)

REM ---------------------------
REM MODE PEMANGGILAN FUNGSI
REM ---------------------------
set "func_name=%1"
shift

set "args="
set "return_to="
:parseargs
if "%1"=="" goto :run
if "%1"==">" (
    shift
    set "return_to=%1"
    shift
    goto :parseargs
)
set "args=!args! %1"
shift
goto :parseargs

:run
REM Ambil isi fungsi sebagai skrip
set "output="
for /f "delims=" %%x in ('python helpers\fungsi.py panggil %func_name% !args! 2^>nul') do (
    call main.bat %%x >> .temp_result.txt
)

REM Tangkap return (jika ada)
if defined return_to (
    for /f "delims=" %%r in (.temp_result.txt) do (
        set "last_line=%%r"
    )
    set "%return_to%=%last_line%"
    del .temp_result.txt >nul 2>&1
) else (
    type .temp_result.txt
    del .temp_result.txt >nul 2>&1
)

endlocal & exit /b 0

:captureFunction
set "line="
:inputLoop
set /p "line=> "
echo %line%
if /i "%line%"=="selesai" goto :eof
goto :inputLoop
