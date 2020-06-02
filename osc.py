
from utils import PrintManager
from printer import Printer 

from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher

import threading
import asyncio

class Network:
    # 
    def __init__(self, listen_port, ip, port):    
        # 
        self.client = -1
        self.server = -1

        # printer reference
        self.printer = None

        #
        self.InitNetwork(ip, port, listen_port)
    
    # network binds the printer to update nozzle poz
    def Bind(self, p: Printer):
        self.printer = p
    
    # 
    def InitNetwork(self, client_ip, client_port, listen_port):
        # client
        self.client = udp_client.SimpleUDPClient(client_ip, client_port)
        PrintManager("Connecting client on port {}.".format(client_port), 4)

        # server callbacks
        dispatch = Dispatcher()
        dispatch.map("/move*", self.MoveNozzle) # /move/extrude and /move
        dispatch.map("/extrude", self.ExtractMaterial)
        dispatch.map("/retract", self.RetractMaterial)
        dispatch.set_default_handler(lambda _: PrintManager("Received message.", 1))
        # TODO: Add other functions


        # server 
        loop = asyncio.get_event_loop()
        self.server = AsyncIOOSCUDPServer(("127.0.0.1", listen_port), dispatch, asyncio.get_event_loop())
        PrintManager("Serving on {}:{}".format("127.0.0.1", listen_port), 4)
        self.server.serve()

        # start the event loop for server
        self.osc_thread = threading.Thread(target=loop.run_forever)
        self.osc_thread.daemon = True
        self.osc_thread.start()


    #
    # Send message to processing
    def SendMessage(self, name, message):
        self.client.send_message(name, message)
        # client.send_message("/filter1", [1., 2.])


    # 
    #   Processing Callbacks
    #
    def isPrinterConnected(self):
        return (self.printer is not None and self.printer.isconnected)
    def MoveNozzle(self, identifier, *args):
        if self.isPrinterConnected():
            if identifier == "/move/extrude":
                self.printer.UpdatePosition(args[0], args[1], args[2], True) # extrude=True
            else:
                self.printer.UpdatePosition(args[0], args[1], args[2])
            # PrintManager("{} x={}, y={}, z={}".format(identifier, args[0], args[1], args[2]), 1)
    #
    def ExtractMaterial(self, identifier, *args):
        if self.isPrinterConnected():
            self.printer.Extract()
    #
    def RetractMaterial(self, identifier, *args):
        if self.isPrinterConnected():
            self.printer.Retract()