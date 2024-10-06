#!/bin/bash

sudo cp -f Telegram-Member-Booster.service /etc/systemd/system/
sudo cp -f Telegram-Member-Booster.timer /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable Telegram-Member-Booster.timer

sudo systemctl start Telegram-Member-Booster.timer
