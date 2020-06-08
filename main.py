
import argparse  # parse arguments
import time

# import files 
from utils import *
from keys import * 
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

    # detect keys
    kb = KBHit()

    # Start printer
    printer = Printer(args.serial)

    # Start OSC network
    net = Network(args.listenport, args.ip, args.port)
    net.Bind(printer)

    # keep track of time
    # starttime=time.time()

    # main loop
    while True:
        # printer obj handles the message transfer internally
        # update Processing sketch about printer state
        # if time.time()-starttime > 2: # second
        #     net.SendMessage("/PY/temp", [printer.bed_temp, printer.bed_temp_target, \
        #         printer.nozzle_temp, printer.nozzle_temp_target])
        #     # TODO: may need to send more frequently
        #     # net.SendMessage("/PY/n_pos", [printer.nozzle_pos[0], printer.nozzle_pos[1], printer.nozzle_pos[2]])
        #     starttime = time.time()

        # Detect keys
        try:
            if kb.kbhit():
                c = kb.getch()
                sc = str(c)

                if ord(c) == 27: # ESC
                    break
                elif sc == "t":
                    if printer.IsPrinterOnline():
                        printer.TemperatureControl(200, 50)
                        PrintManager("Temperature set to n={} b={}".format(200, 50), 1)                
                elif sc == "r":
                    if printer.IsPrinterOnline():
                        printer.PreparePrinter()
                        PrintManager("Prepare printer", 1)
                elif sc == "e":
                    if printer.IsPrinterOnline():
                        printer.ExtrudeOnSide(random.random()+0.2)
                        PrintManager("Extruding on side", 1)
        except UnicodeDecodeError: pass
        except KeyboardInterrupt:
            break
    
    # reset keyboard
    kb.set_normal_term()

    printer.Retract()
    printer.SendFinish()
    printer.Destroy()