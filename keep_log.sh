# Get Linux notification and loged
# https://askubuntu.com/a/770249

#!/bin/bash

logfile=$1

dbus-monitor "interface='org.freedesktop.Notifications'"|grep --line-buffered "Login code" >> "notif.log"

#printf "---$( date )---\n"{}"\n" >> "notif.log"