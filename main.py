


## TODO:
# get list of ports for connection
# listener for succesful connection
# Readme (printrun build and lighter gcode parser)



# append sister directory to sys.path so that we can import printcore
import sys, os
sys.path.append(os.path.abspath('Printrun/'))
from printrun.printcore import printcore

# detect keys (windows)
import msvcrt

# utility functions
from utils import *

# 
# from printrun import gcoder

##
## Connects to the Ender 3 Pro
port = 'COM4'
p = printcore(port, 115200)
print("Connecting printer on port {}. Press R to auto home.".format(port))

x = 0.0
y = 0.0
z = 0.0

while 1:
    #p.send_now("M105") # this will send M105 immediately, ahead of the rest of the print
    
    # esc
    if msvcrt.kbhit():
        ch = msvcrt.getch()
        # escape if ESC
        if ord(ch) == 27:
            break
        
        if p.online:
            p.send("G0 X{} Y{} Z{}".format(x,y,z))
        
        if ch == b'r':
            p.send("G28")
            x = 0
            y = 0
            z = 0
        
        step = 0.5
        if ch == b'x':
            x += step
        if ch == b's':
            x -= step
        if ch == b'y':
            y += step
        if ch == b'h':
            y -= step
        if ch == b'z':
            z += step
        if ch == b'a':
            z -= step
        
        x = constrain(x, 0,150)
        y = constrain(y, 0,150)
        z = constrain(z, 0,150)
        
        print("x={}, y={}, z={}".format(x,y,z))

p.cancelprint() # cancels the current print
p.disconnect() # disconnect from the printer once you are done. This will also stop running prints.


########
# use these to pause/resume the current print
#p.pause()
#p.resume()           

# gcode loader and starting print 
#gcode=[i.strip() for i in open('filename.gcode')] # or pass in your own array of gcode lines instead of reading from a file
#gcode = gcoder.LightGCode(gcode)
#p.startprint(gcode) # this will start a print