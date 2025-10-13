source /home/filmanetskap/skap/skap/bin/activate

# Start main.py i bakgrunnen
cd /home/filamentskap/skap/Filamentskap
python3 core/main.py &

# Kjør GUI i forgrunnen
cd /home/filamentskap/skap/Filamentskap
python3 application/gui_main.py