#!/bin/bash
# start_dashboard.sh

# Sett arbeidskatalog til prosjektmappa
cd /home/pi/path/to/your/project

# Eksporter eventuelle miljøvariabler (f.eks. for virtualenv)
# export VIRTUAL_ENV=/home/pi/venv
# source $VIRTUAL_ENV/bin/activate

# Start Flask-appen i bakgrunnen
nohup python3 app.py > flask.log 2>&1 &

# Gi Flask et par sekunder til å starte opp
sleep 2

# Start sensor-scriptet i bakgrunnen
nohup python3 main.py > sensor.log 2>&1 &

# Gi scriptet et par sekunder
sleep 2

# Åpne Chromium i kiosk-modus mot lokal Flask
/usr/bin/chromium-browser --noerrdialogs --kiosk http://localhost:5000

# (Chromium vil holde seg i front; når du lukker Chromium, stopper hele scriptet.)
