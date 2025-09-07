@echo off
REM modules/masukkan.bat

python helpers\masukkan.py %*
exit /b %ERRORLEVEL%
