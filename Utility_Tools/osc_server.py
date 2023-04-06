from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient
import threading


class OSCBootServer:
    def __init__(self, ip_address, port, dispatcher, socketio_client):
        self.ip_address = ip_address
        self.port = port
        self.dispatcher = dispatcher
        self.threading_server = ThreadingOSCUDPServer((self.ip_address, self.port), self.dispatcher)
        self.supercollider_ready = False
        self.processing_ready = False
        self.socketio_client = socketio_client

    def print_processing_ready(self, address, *args):
        print(f"Processing {address}: {args}")
        self.processing_ready = True
        self.shut_down()

    def print_supercollider_ready(self, address, *args):
        print(f"SuperCollider {address}: {args}")
        self.supercollider_ready = True
        self.shut_down()

    def shut_down(self):
        if self.processing_ready == True and self.supercollider_ready == True:
            print("Processing and Supercollider booted, shutting osc server down and running movement...")
            self.threading_server.shutdown()
            return self.socketio_client
        else:
            pass

    def handle_request(self):
        self.threading_server.handle_request()

    def serve_forever(self):
        self.threading_server.serve_forever()


def run_osc_boot_server():
    dispatcher = Dispatcher()
    osc_server = OSCBootServer("127.0.0.1", 12645, dispatcher, True)
    osc_server.dispatcher.map("/processing_ready", osc_server.print_processing_ready)
    osc_server.dispatcher.map("/supercollider_ready", osc_server.print_supercollider_ready)
    osc_server.dispatcher.map("/shutdown", osc_server.shut_down)
    thread = threading.Thread(target=osc_server.serve_forever)
    thread.start()


run_osc_boot_server()

# if __name__ == "__main__":
#     # dispatcher = Dispatcher()
#     # osc_server = OSCBootServer("127.0.0.1", 12645, dispatcher)
#     # osc_server.dispatcher.map("/processing_ready", osc_server.print_processing_ready)
#     # osc_server.dispatcher.map("/supercollider_ready", osc_server.print_supercollider_ready)
#     # osc_server.dispatcher.map("/shutdown", osc_server.shut_down)
#
#     #
#     # thread = threading.Thread(target=osc_server.serve_forever)
#     # thread.start()
#     # run_osc_boot_server()
#     #
#     # client = SimpleUDPClient("127.0.0.1", 12645)
#     #
#     # client.send_message("/processing_ready", True)
#
#     # client.send_message("/supercollider_ready", True)
