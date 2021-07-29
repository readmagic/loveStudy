@echo off
chcp 65001
REM 模拟器路径
start C:\"Program Files (x86)"\MuMu\emulator\nemu\EmulatorShell\NemuPlayer.exe


interface portproxy add v4tov4 listenport=5555 listenaddress=172.16.24.80 connectport=7555 connectaddress=127.0.0.1
pause