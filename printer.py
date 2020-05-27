import sys, os

# append sister directory to sys.path so that we can import printcore
sys.path.append(os.path.abspath('Printrun/'))

# Printrun
from printrun.printcore import printcore
from printrun import gcoder

class Printer:
    # main printer instance
    printer = -1

    #
    # Constructs printer obj 
    def __init__(self, port):
        self.InitPrinter(port)

    # Connects to the Ender 3 Pro
    def InitPrinter(self, port):
        self.printer = printcore(port, 115200) # port = 'COM4'
        print("Connecting printer on port {}.".format(port))

    #         
    def Destroy(self):
        self.printer.cancelprint() # cancels the current print
        self.printer.disconnect() # disconnect from the printer once you are done. This will also stop running prints.

    # 
    def StartPrintWithGCode(self, gcode):
        gcode = gcoder.LightGCode(gcode)
        print("STARTING GCODE: " + gcode)
        # self.printer.startprint(gcode) # this will start a print

    # 
    def PausePrint(self):
        self.printer.pause()
    def ResumePrint(self):
        self.printer.resume()

    #
    # check if connected
    def IsPrinterOnline(self):
        return (self.printer != -1 and self.printer.online)


    #
    def SendLine(self, line):
        if self.IsPrinterOnline():
            # printer.send(line)
            print("SENDING TO PRINTER: " + line)


    # 
    def SendAutoHome(self):
        self.SendLine("G28")