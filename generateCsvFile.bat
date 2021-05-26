@echo off

:: remember the current directory
set CUR=%~dp0

:: check if the input file name is .txt
if "%~x1" neq ".txt" (
  echo "Unexpected input file name: %1"
  pause
  exit
)

set /P TIMING="Input the start time:"

cd /d %~dp0
python OutCsvELAN.py %1 %TIMING% >> genCsvLog.log

pause
