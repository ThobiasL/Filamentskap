@echo off
REM run_dashboard.bat

REM 1) Gå til prosjektmappa
cd /d "C:\Users\YourUsername\Documents\Filamentskap"

REM 2) (Valgfritt) Aktiver virtuell miljø hvis du bruker venv
call venv\Scripts\activate.bat

REM 3) Start Flask-server i eget vindu
start "Flask Server" cmd /k "python C:\Users\YourUsername\Documents\Filamentskap\adapters\app_adapter.py"

REM Gi Flask et par sekunder til å starte opp
timeout /t 3 /nobreak >nul

REM 4) Åpne Chrome i kiosk-modus
REM Juster banen til chrome.exe om nødvendig
set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
start "" %CHROME_PATH% --noerrdialogs --kiosk http://localhost:5000

exit
