
import re
import math
import random
import sys, os

#
REPORT_NONE = 0
REPORT_POS = 1
REPORT_TEMP = 2
REPORT_MANUAL = 4

#
lineignorepattern = re.compile("ok ?\d*$|.*busy: ?processing|.*busy: ?heating|.*Active Extruder: ?\d*$")
tempreading_exp = re.compile("(^T:| T:)")
tempreport_exp = re.compile("([TB]\d*):([-+]?\d*\.?\d*)(?: ?\/)?([-+]?\d*\.?\d*)")
def parse_temperature_report(report):
    matches = tempreport_exp.findall(report)
    return dict((m[0], (m[1], m[2])) for m in matches)



#
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

# 
# Console print manager
# 'level' is importance of the message: [0, 4]
def PrintManager(message, level=4): 
    level = constrain(level, 0, 4)
    prefix = ""
    if level is 4:  
        prefix = "#####\t"
    elif level is 3:
        prefix = " ####\t"
    elif level is 2:
        prefix = "  ###\t"
    elif level is 1:
        prefix = "   ##\t"
    else:
        prefix = "    #\t"

    print(prefix+" "+message)