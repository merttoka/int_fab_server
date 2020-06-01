
# import re
import math
import random
import sys, os

# if os.name == 'posix': # mac-linux
#     import tty        
# elif os.name == 'nt': # windows
#     import msvcrt 

# # detect keys
# def DetectKey():
#     if os.name == 'posix': # mac-linux
#         try:
#             ch = sys.stdin.read(1)
#             if ch:
#                 return repr(ch), ord(ch)
#         except IOError: pass
#     elif os.name == 'nt': # windows
#         if msvcrt.kbhit():
#             ch = msvcrt.getch()
#             return repr(ch), ord(ch)
#     return '', 0














#
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


# lineignorepattern = re.compile("ok ?\d*$|.*busy: ?processing|.*busy: ?heating|.*Active Extruder: ?\d*$")
# tempreading_exp = re.compile("(^T:| T:)")
# tempreport_exp = re.compile("([TB]\d*):([-+]?\d*\.?\d*)(?: ?\/)?([-+]?\d*\.?\d*)")
# def parse_temperature_report(report):
#     matches = tempreport_exp.findall(report)
#     return dict((m[0], (m[1], m[2])) for m in matches)

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