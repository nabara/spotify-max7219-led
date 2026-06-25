#!/bin/bash
# Continuously polls the currently playing Spotify track and
# scrolls "<artist> - <title>" across the MAX7219 LED matrix.
#
# This version cd's into its own directory first, so it works
# regardless of where it is launched from (e.g. from cron @reboot).

cd "$(dirname "$0")" || exit 1

CURRENT=""
TEXT=""
while true; do
    TEXT=$(sudo python3 nowplaying.py)
    if [ "$TEXT" = 0 ]; then
        sudo python3 view_message.py -t " "
    else
        sudo python3 view_message.py -t "$TEXT"
        # echo $TEXT
    fi
    sleep 15
done
