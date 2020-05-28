import sys, os
from utils import *

# append sister directory to sys.path so that we can import printcore
sys.path.append(os.path.abspath('Printrun/'))

# Printrun
from printrun.printcore import printcore
from printrun import gcoder

class Printer:

    #
    # Constructs printer obj 
    def __init__(self, port):
        #
        self.printer = -1        # main printer instance
        self.isconnected = False # connection
        self.port = 0            # serial port

        # 
        # nozzle head position
        self.pos = [0, 0, 0]
        self.prev_pos = [0, 0, 0]

        # 
        self.bed_temp = 0
        self.bed_temp_target = 0
        self.nozzle_temp = 0
        self.nozzle_temp_target = 0

        # 
        self.first_layer_height = 0.4
        self.current_height = self.first_layer_height
        self.layer_index = 0

        #
        self.layer_height = 0.3
        self.nozzle_width = 0.4
        self.ret_amount = 6.0
        self.ret_speed = 1200
        self.print_speed = 500
        self.print_speed_high = 1300


        #
        # starts the printer connection
        self.InitPrinter(port)

    # Connects to the Ender 3 Pro
    def InitPrinter(self, port):
        self.port = port
        self.printer = printcore(port, 115200)    # port = 'COM4'
        self.printer.recvcb = self.__Receive_     # listen for messages from printer
        self.printer.onlinecb = self.__Connected_ # on connection
        
    #         
    def Destroy(self):
        self.isconnected = False

        self.printer.cancelprint() # cancels the current print
        self.printer.disconnect() # disconnect from the printer once you are done. This will also stop running prints.

    # 
    # def StartPrintWithGCode(self, gcode):
    #     gcode = gcoder.LightGCode(gcode)
    #     PrintManager("STARTING GCODE: " + gcode, 4)
        # self.printer.startprint(gcode) # this will start a print

    # 
    def PausePrint(self):
        self.printer.pause()
    def ResumePrint(self):
        self.printer.resume()

    #
    def IsPrinterOnline(self):
        return (self.printer != -1 and self.isconnected and self.printer.online)

    #
    def SendLine(self, line):
        if self.IsPrinterOnline():
            self.printer.send(line)
            PrintManager("SENDING TO PRINTER: " + line, 1)
        else:
            PrintManager("PRINTER IS NOT CONNECTED. FAILED TO SEND:  " + line, 4)
    #
    def SendLines(self, lines):
        for line in lines:
            self.SendLine(line)

    #
    # jacob 594x w4
    def MakeRetraction(self, amount, speed, sign):
        mes = ""
        if(sign == -1):
            mes = " ; Retraction"
        else:
            mes = " ; Extraction"
        return "G1 F" + str(speed) + " E" + str(sign * amount) + mes

    # 
    def UpdateNozzlePosition(self, _x, _y, _z, extrude_flag=False):
        self.prev_pos = self.pos
        self.pos = [_x, _y, self.first_layer_height] # _z] 

        self.MoveNozzle(extrude_flag)


    #
    # Higher level functions
    # 

    #
    def Extract(self):
        self.SendLine(self.MakeRetraction(self.ret_amount, self.ret_speed, 1))
    def Retract(self):
        self.SendLine(self.MakeRetraction(self.ret_amount, self.ret_speed, -1))
    #
    def MoveNozzle(self, isextrude=False):
        to = self.pos
        fr = self.prev_pos
        if isextrude:
            p = [to[0]-fr[0], to[1]-fr[1], to[2]-fr[2]]
            
            l = math.sqrt(p[0]*p[0]+p[1]*p[1]+p[2]*p[2])
            numerator = (self.nozzle_width * l * self.layer_height)
            denominator = (1.75 / 2) * (1.75 / 2) * math.pi
            
            e = numerator / denominator
            
            self.SendLine("G1 F" + str(self.print_speed) + \
                          " E"+ "{:.{}f}".format(e,8) + \
                          " X" + "{:.{}f}".format(to[0],2) + \
                          " Y" + "{:.{}f}".format(to[1],2) + \
                          " Z" + "{:.{}f}".format(to[2],2))
        else:
            self.SendLine("G1 F" + str(self.print_speed) + \
                          " X" + "{:.{}f}".format(to[0],2) + \
                          " Y" + "{:.{}f}".format(to[1],2) + \
                          " Z" + "{:.{}f}".format(to[2],2))
        

    # 
    def SendAutoHome(self):
        self.SendLine("G28") # home x y z 
        self.SendLine("G92 E0") # home extruder

    #
    # jacob 594x w4
    def TemperatureControl(self, nozzle=200, bed=50):
        sb = []

        sb.append("M140 S" + str(bed) +" ; Set Bed Temperature")
        sb.append("M105")
        sb.append("M190 S" + str(bed) +" ; Wait for Bed Temperature")
        sb.append("M104 S" + str(nozzle) +" ; Set Nozzle Temperature")
        sb.append("M105")
        sb.append("M109 S" + str(nozzle) +" ; Wait for Nozzle Temperature")

        self.SendLines(sb)

    # 
    # jacob 594x w4
    def PreparePrinter(self):
        self.SendAutoHome()
        self.SendLine("M83") # E relative
        self.SendLine("G90") #nice absolute 
        self.SendLine("G1 F300 Z"+str(self.first_layer_height)) # 
        
        # extrude initial material
        self.SendLine("G1 X10 Y110 E8 F800")
        self.SendLine("G1 X10.03 Y110 E8 F800")
        self.SendLine("G1 X10.03 Y10 E8 F800")

        self.Retract()



    #
    # Private callback functions from printer to python
    # 
    def __Connected_(self):
        PrintManager("Connected printer on port {}. Preparing printer...".format(self.port), 4)

        # Initialize settings on printer
        self.isconnected = True
        self.TemperatureControl(200, 50)
        self.PreparePrinter()

    def __Receive_(self, l):
        l = l.rstrip()

        # TODO: parse and Send this to processing 
        PrintManager("ACK: "+ l, 0)