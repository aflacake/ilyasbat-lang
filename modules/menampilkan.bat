@echo off
REM modules/menampilkan.bat

setlocal EnableDelayedExpansion
set var=%1

python helpers\menampilkan.py %var%
