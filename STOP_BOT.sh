#!/bin/bash
# Остановка старого процесса бота

# Найти процесс бота по имени файла
pkill -f "bot_main.py"

# Или найти и остановить по PID
# ps aux | grep bot_main.py | grep -v grep | awk '{print $2}' | xargs kill

# Если запущен через screen/tmux
# screen -X -S bot quit
# tmux kill-session -t bot

# Если запущен как systemd service
# systemctl stop school_test_bot

echo "Процесс бота остановлен"

