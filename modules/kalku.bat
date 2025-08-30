@echo off
setlocal enabledelayedexpansion

set "line=%*"
for /f "tokens=1,2,3,4,5 delims= " %%a in ("%line%") do (
    set "var=%%a"
    set "equal=%%b"
    set "val1=%%c"
    set "op=%%d"
    set "val2=%%e"
)

for /f "delims=" %%r in ('python helpers\kalku.py !val1! !op! !val2!') do (
    endlocal & set "%var%=%%r"
)
