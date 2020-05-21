import sys, os
sys.path.append(os.path.abspath('Printrun/'))
from printrun.printcore import printcore
import msvcrt
#from printrun import gcoder

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

p = printcore('COM4',115200) # or p.printcore('COM3',115200) on Windows

#gcode=[i.strip() for i in open('filename.gcode')] # or pass in your own array of gcode lines instead of reading from a file
#gcode = ["G0 X20 Y86 Z90", "G0 F500 X180 Y6 Z70", "G0 F2000 X30 Y60 Z14"]

#gcode = gcoder.LightGCode(gcode)

#p.startprint(gcode) # this will start a print

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

#p.pause() # use these to pause/resume the current print
#p.resume()           
p.cancelprint() # cancels the current prints
p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.
