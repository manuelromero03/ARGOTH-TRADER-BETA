@echo off
cd /d "%~dp0"
call .venv/Scripts/activate.bat
python auto_commit_pro_v6.py 
pause

