
import argparse  # parse arguments

# detect keys
from sneakysnek.recorder import Recorder
from sneakysnek.keyboard_keys import KeyboardKey
from sneakysnek.keyboard_event import KeyboardEvents

# import files 
from utils import *
from printer import Printer
from osc import Network

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=12000, help="The port the OSC server is listening on")
    parser.add_argument("--listenport", type=int, default=5876, help="The port to listen on")
    parser.add_argument("--serial", default="COM4", help="The serial port that 3D Printer is using")
    args = parser.parse_args()

    # key callback 
    isEsc = False
    isR   = False
    def HandleKey(event):
        global isEsc, isR
        # print(event)
        if event.event is KeyboardEvents.DOWN:
            if event.keyboard_key == KeyboardKey.KEY_ESCAPE:
                isEsc = True
            elif event.keyboard_key == KeyboardKey.KEY_R:
                isR = True
    # record keys
    recorder = Recorder.record(HandleKey)

    # Start printer
    printer = Printer(args.serial)

    # Start OSC network
    net = Network(args.listenport, args.ip, args.port)
    net.Bind(printer)

    # main loop
    while not isEsc:
        # printer obj handles the message transfer internally

        # 
        if isR and printer.IsPrinterOnline():
            printer.SendAutoHome()
            PrintManager("Autohome sent", 1)
            isR = False

    recorder.stop()

    printer.Retract()
    printer.SendHigh()
    printer.Destroy()