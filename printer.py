from utils import *

# append sister directory to sys.path so that we can import printcore
sys.path.append(os.path.abspath('Printrun/'))

# Printrun
from printrun.printcore import printcore
from printrun import gcoder

import queue

class Printer:

    #
    # Constructs printer obj 
    def __init__(self, port):
        #
        self.printer = -1        # main printer instance
        self.isconnected = False # connection
        self.port = 0            # serial port

        # 
        # TODO: nozzle head positions
        self.pos = [0, 0, 0]
        self.prev_pos = [0, 0, 0]

        # TODO: printer messages queue
        # correspond every line with an acknowlegment
        self.ack_queue = queue.Queue()

        #
        self.nozzle_pos = [0,0,0]

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
        self.layer_height = 0.4
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
        self.printer = printcore(port, 115200)    # port = 'COM#' in windows 
        self.printer.onlinecb = self.__Connected_ # on connection
        self.printer.recvcb = self.__Receive_     # listen for messages from printer
        
    #         
    def Destroy(self):
        self.isconnected = False

        self.printer.cancelprint() # cancels the current print
        self.printer.disconnect() # disconnect from the printer once you are done. This will also stop running prints.

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
            PrintManager("SENT TO PRINTER: " + line, 1)
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
    def UpdatePosition(self, _x, _y, _z, extrude_flag=False):
        if not extrude_flag:
            self.pos = self.prev_pos = [_x, _y, _z] 
        else:
            self.prev_pos = self.pos
            self.pos = [_x, _y, _z] 

        self.MoveNozzle(extrude_flag)


    #
    #  Higher level functions
    # # # # # # #  # # # # # # #

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
            # jacob 594x w4
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
            self.SendLine("G0 F" + str(self.print_speed_high) + \
                          " X" + "{:.{}f}".format(to[0],2) + \
                          " Y" + "{:.{}f}".format(to[1],2) + \
                          " Z" + "{:.{}f}".format(to[2],2))
    
    # 
    def SendAutoHome(self):
        self.SendLine("G28") # home x y z 
        self.SendLine("G92 E0") # home extruder

    #
    def SendFinish(self):
        self.SendLine("G0 X0 Y200 Z30 E-6") 

    # 
    def ExtrudeOnSide(self, scale=1):
        scale = constrain(scale, 0.2, 2)

        _x = scale * 10
        _y = scale * 100
        self.SendLine("G0 X" + "{:.{}f}".format(_x,2) +" Y" + "{:.{}f}".format(_x,2) +" Z0.4 F800")
        self.Extract()
        self.SendLine("G1 X" + "{:.{}f}".format(_x,2) +" Y" + "{:.{}f}".format(_y+_x,2) +" Z0.4 E8 F800")
        self.SendLine("G1 X" + "{:.{}f}".format(_x+0.4*scale,2) +" Y" + "{:.{}f}".format(_y+_x,2) +" Z0.4 E0.02 F800")
        self.SendLine("G1 X" + "{:.{}f}".format(_x+0.4*scale,2) +" Y" + "{:.{}f}".format(_x,2) +" Z0.4 E8 F800")
        self.Retract()

    #
    # jacob 594x w4
    def TemperatureControl(self, nozzle=200, bed=50):
        self.SendLine("M140 S" + str(bed) +" ; Set Bed Temperature")
        self.UpdateTemperature()
        self.SendLine("M190 S" + str(bed) +" ; Wait for Bed Temperature")
        self.SendLine("M104 S" + str(nozzle) +" ; Set Nozzle Temperature")
        self.UpdateTemperature()
        self.SendLine("M109 S" + str(nozzle) +" ; Wait for Nozzle Temperature")

    # reports temperature without heating
    def UpdateTemperature(self):
        self.SendLine("M105")
    # reports nozzle position
    def UpdateNozzlePosition(self):
        self.SendLine("M114")

    # 
    # jacob 594x w4
    def PreparePrinter(self):
        self.SendAutoHome()
        self.SendLine("M83") # E relative
        self.SendLine("G90") # absolute 
        self.SendLine("G0 F300 E0 Z"+str(self.first_layer_height)) # 
        
        # extrude initial material
        self.ExtrudeOnSide()


    #
    #   Private callback functions from printer to python
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def __Connected_(self):
        PrintManager("Connected printer on port {}.".format(self.port), 4)
        PrintManager("Press 'T' for temperature conrols (b=50, n=200).", 3)
        PrintManager("      'R' for reseting printer (auto home, move to first layer, 'E'xtrude on side)", 3)
        PrintManager("      'E' for extruding material on the side", 3)
        
        # Initialize settings on printer
        self.isconnected = True
        self.UpdateTemperature()
        self.UpdateNozzlePosition()

    # Message from printer
    def __Receive_(self, l):
        l = l.rstrip()

        # ack_queue.put
        # TODO: parse and Send this to processing 
        PrintManager("ACK: "+ l, 1)   

        if not self.recvcb_actions(l):
            report_type = self.recvcb_report(l)
            #
            PrintManager("ReportType={}".format(report_type), 1)
            if report_type & REPORT_POS:
                m114_res = gcoder.m114_exp.findall(l)
                self.nozzle_pos = [float(m114_res[0][1]), float(m114_res[1][1]), float(m114_res[2][1])]
                #
                PrintManager("UPDATE NOZZLE POS: [{},{},{}]".format(self.nozzle_pos[0], self.nozzle_pos[1], self.nozzle_pos[2]), 0)
            if report_type & REPORT_TEMP:
                self.update_tempreading(l)
                #
                PrintManager("UPDATE TEMP READINGS: b={}/{} n={}/{}".format(self.bed_temp, self.bed_temp_target, self.nozzle_temp, self.nozzle_temp_target), 0)
            if not lineignorepattern.match(l) and l[:4] != "wait" \
                 and (report_type == REPORT_NONE or report_type & REPORT_MANUAL):
                if l[:5] == "echo:":
                    l = l[5:].lstrip()
                #
                PrintManager("\r" + l.ljust(15), 1)

    ## PARSE INCOMING MESSAGE
    def recvcb_report(self, l):
        isreport = REPORT_NONE
        if "ok C:" in l or "Count" in l \
           or ("X:" in l and len(gcoder.m114_exp.findall(l)) == 6):
            isreport = REPORT_POS
            # if self.userm114 > 0:
            #     self.userm114 -= 1
            #     isreport |= REPORT_MANUAL
        if "ok T:" in l or tempreading_exp.findall(l):
            self.tempreadings = l
            isreport = REPORT_TEMP
            # if self.userm105 > 0:
            #     self.userm105 -= 1
            #     isreport |= REPORT_MANUAL
            # else:
            #     self.m105_waitcycles = 0
        return isreport

    def recvcb_actions(self, l):
        if l.startswith("!!"):
            # self.do_pause(None)
            msg = l.split(" ", 1)
            #
            PrintManager("recvcb actions !! " + msg, 3)
            # if len(msg) > 1 and self.silent is False: self.logError(msg[1].ljust(15))
            # sys.stdout.write(self.promptf())
            # sys.stdout.flush()
            return True
        elif l.startswith("//"):
            command = l.split(" ", 1)
            #
            PrintManager("recvcb actions // " + command, 3)
            if len(command) > 1:
                command = command[1]
                #
                PrintManager("Received command {}".format(command), 2)
                command = command.split(":")
                if len(command) == 2 and command[0] == "action":
                    command = command[1]
                    if command == "pause":
                        #
                        PrintManager("PAUSE", 1)
                        # self.do_pause(None)
                        # sys.stdout.write(self.promptf())
                        # sys.stdout.flush()
                        return True
                    elif command == "resume":
                        #
                        PrintManager("RESUME", 1)
                        # self.do_resume(None)
                        # sys.stdout.write(self.promptf())
                        # sys.stdout.flush()
                        return True
                    elif command == "disconnect":
                        #
                        PrintManager("DISCONNECT", 1)
                        # self.do_disconnect(None)
                        # sys.stdout.write(self.promptf())
                        # sys.stdout.flush()
                        return True

    ## UPDATE TEMPERATURE READINGS
    def update_tempreading(self, tempstr):
        temps = parse_temperature_report(tempstr)
        if "T0" in temps and temps["T0"][0]: hotend_temp = float(temps["T0"][0])
        elif "T" in temps and temps["T"][0]: hotend_temp = float(temps["T"][0])
        else: hotend_temp = None
        if "T0" in temps and temps["T0"][1]: hotend_setpoint = float(temps["T0"][1])
        elif "T" in temps and temps["T"][1]: hotend_setpoint = float(temps["T"][1])
        else: hotend_setpoint = None
        if hotend_temp is not None:
            self.nozzle_temp = hotend_temp
            if hotend_setpoint is not None:
                self.nozzle_temp_target = hotend_setpoint
        bed_temp = float(temps["B"][0]) if "B" in temps and temps["B"][0] else None
        if bed_temp is not None:
            self.bed_temp = bed_temp
            setpoint = temps["B"][1]
            if setpoint:
                self.bed_temp_target = float(setpoint)