@echo off
NET SESSION >nul 2>&1
if %ERRORLEVEL% equ 0 (
    if exist "%temp%\kon_dir_path.txt" (
        goto :payload
    ) else (
    goto :heh
    )
) else (
    cd > %temp%\kon_dir_path.txt
)


:getadmin
    echo %~nx0: elevating self
    set vbs=%temp%\getadmin.vbs
    echo Set UAC = CreateObject^("Shell.Application"^)                >> "%vbs%"
    echo UAC.ShellExecute "%~s0", "payload %~sdp0 %*", "", "runas", 1 >> "%vbs%"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
goto :eof


:payload
set /p VAR=<%temp%\kon_dir_path.txt
cd %VAR%
del "%temp%\kon_dir_path.txt"
:heh
python main.py