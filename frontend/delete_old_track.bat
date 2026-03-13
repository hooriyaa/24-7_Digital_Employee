@echo off
cd /d "%~dp0"
rmdir /s /q "app\track\[ticketId]"
echo Deleted [ticketId] folder
pause
