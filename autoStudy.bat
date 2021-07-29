@echo off
chcp 65001
REM 模拟器路径
start C:\"Program Files (x86)"\MuMu\emulator\nemu\EmulatorShell\NemuPlayer.exe
adb kill-server
adb connect 127.0.0.1:7555
pause