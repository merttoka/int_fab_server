
from pythonosc import udp_client

from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher

import threading
import asyncio
import math

class Network:
    
    # 
    client = -1
    server = -1

    dispatch = -1

    # 
    def __init__(self, listen_port, ip, port):
        self.InitNetwork(ip, port, listen_port)
    
    # 
    def InitNetwork(self, client_ip, client_port, listen_port):
        # client
        self.client = udp_client.SimpleUDPClient(client_ip, client_port)
        print("Connecting client on port {}.".format(client_port))

        # server callbacks
        dispatch = Dispatcher()
        dispatch.map("/test_pde", self.PrintMessage)
        dispatch.set_default_handler(lambda _: print("Received message."))
        # TODO: Add other functions


        # server 
        loop = asyncio.get_event_loop()
        self.server = AsyncIOOSCUDPServer(("127.0.0.1", listen_port), dispatch, asyncio.get_event_loop())
        print("Serving on {}:{}".format("127.0.0.1", listen_port))
        self.server.serve()

        # start the event loop for server
        self.osc_thread = threading.Thread(target=loop.run_forever)
        self.osc_thread.daemon = True
        self.osc_thread.start()

    #
    # Send message to client
    def SendMessage(self, message):
        self.client.send_message("/test_py", message)
        # client.send_message("/filter1", [1., 2.])

    # 
    # Listen Callbacks
    def PrintMessage(self, identifier, *args):
        print("{} x={}, y={}, z={}".format(identifier, args[0], args[1], args[2]))