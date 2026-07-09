@echo off
setlocal

call "%~dp0run.bat" --model small.en --no-vad %*

endlocal
