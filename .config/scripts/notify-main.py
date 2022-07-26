#!/usr/bin/env python
#  
#  by mdfk <mdfk@Elite>

import os, sys

# Arguments modelate
# ./notifty-main <program> <inc/dec/set> <value>

# Values 
modifier= 3

# Functions
def exec_and_notify(status,value):
    # Dictionaires                                       e.g inc cmd: xbacklight -inc N / amixer sset Master N%+
    backlight = {"program":"xbacklight",
                     "inc":f"-inc {value}",              #========> inc/dec gradually
                     "dec":f"-dec {value}",              #        
                     "set":f"-set {sys.argv[3]}"}        #==> Set direct e.g: 75% (day) or 25% (night)
    volume = {"program":"amixer",
                  "inc":f"sset Master {value}%+",        #========> inc/dec gradually
                  "dec":f"sset Master {value}%-",        #          
                  "set":f"sset Master {sys.argv[3]}%"}   #========> Set direct e.g: 15% (calm), 70% (party) or toggle (on/off)

    # Command
    if sys.argv[1] == "backlight":
        command = f"{backlight['program']} {backlight[sys.argv[2]]}"
    elif sys.argv[1] == "volume":
        command = f"{volume['program']} {volume[sys.argv[2]]} > /dev/null"

    os.system(f"{command}")
    dunstify_cmd = f"dunstify -a '{sys.argv[1].capitalize()}' '{sys.argv[2].capitalize()}: {status}%' \
                   -i '~/.icons/{sys.argv[1]}-{sys.argv[2]}.png' -h string:x-dunst-stack-tag:{sys.argv[1]}"
    if status.isdigit():
        dunstify_cmd += f" -h 'int:value:{status}'"
    os.system(dunstify_cmd)

def status_range(value,status,iterator):
    if sys.argv[2] == "dec" or sys.argv[2] == "inc":
        value = int(value)
        for n in range(0,value,iterator):
            if (1+iterator) <= status and sys.argv[2] == "dec":
                status -= iterator
            elif status <= (100-iterator) and sys.argv[2] == "inc":
                status += iterator
            elif sys.argv[2] == "dec":
                iterator = status-1%iterator
                status -= status-1%iterator
            exec_and_notify(str(status),iterator)
    else:
        exec_and_notify(sys.argv[3],sys.argv[3])

def get_icon(program,status):
    if status <= 25:
        return f"{program}-low.png"
    if status < 50:
        return f"{program}-medium.png"
    if status < 75:
        return f"{program}-good.png"
    else:
        return f"{program}-high.png"

# Conditionals
if sys.argv[1] == 'backlight':
    status = int(os.popen('xbacklight | cut -d "." -f1').read())
    status_range(sys.argv[3],status,modifier)

elif sys.argv[1] == 'volume':
    status = int(os.popen("amixer sget Master | grep Left: | awk -F '[][]' '{ print $2 }' | cut -d '%' -f1").read())
    status_range(sys.argv[3],status,modifier)

else:
    print(f"Error option {sys.argv[1]} not correct")

