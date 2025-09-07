@echo off
REM modules/impor.bat

python helpers\impor.py %*
exit /b %ERRORLEVEL%
