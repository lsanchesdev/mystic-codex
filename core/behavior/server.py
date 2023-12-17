from core.communicator import Communicator
from core.gatekeeper import Gatekeeper
from core.memory import Memory
from enums.grappler_type import GrapplerType
from modules.game import Game
from modules.player import Player
import socket, sys, json
import importlib


class ServerBehavior:

    def __init__(self, codex):
        super().__init__()
        self.codex = codex
        self.socket = None

    def run(self):
        # Attach Grappler to running Process
        self.codex.grappler.attachTo(self.codex.parameters, GrapplerType.PROCESS)

        # Initialize Modules
        self.codex.memory = Memory(self.codex)
        self.codex.gatekeeper = Gatekeeper(self.codex)
        self.codex.communicator = Communicator(self.codex)
        self.codex.player = Player(self.codex)
        self.codex.game = Game(self.codex)

        # Initialize socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.codex.parameters['server']['ip'], self.codex.parameters['server']['port']))
        self.socket.listen(1)

        # Log Message
        print("Codex Server is waiting for connections on ",
              str(self.codex.parameters['server']['ip']) + ":" + str(self.codex.parameters['server']['port']))

        # Run main loop
        self.main()

    def main(self):
        self.socket.settimeout(1.0)  # Set a timeout of 1 second

        try:
            while True:
                try:
                    client_socket, addr = self.socket.accept()
                except KeyboardInterrupt:
                    self.stop()
                except socket.timeout:
                    continue  # Continue the loop even if it times out

                print(f"Connected to {addr}")

                try:
                    while True:
                        # Receive command from the client
                        command = client_socket.recv(1024).decode()
                        if not command:
                            break  # Break the inner loop if the client disconnects

                        print(f"Received command: {command}")

                        # Inside the while loop where you receive the command
                        try:
                            data = json.loads(command)

                            if data["command"] == "Memory.read":
                                # Set Variables
                                address = data["address"]
                                size = data.get("size", 4)

                                # Set Response
                                response = self.codex.memory.read(address, size)
                            elif data["command"] == "Memory.readFromBase":
                                # Set Variables
                                address = data["address"]
                                size = data.get("size", 4)
                                is_pointer = data.get("is_pointer", bool)

                                # Set Response
                                response = self.codex.memory.readFromBase(address, size, is_pointer)
                            elif data["command"] == "Memory.readList":
                                # Set Variables
                                base_address = data["base_address"]
                                first_element_address = data["first_element_address"]

                                # Set Response
                                response = self.codex.memory.readFromList(base_address, first_element_address)
                            elif data["command"] == "Grappler.getProcessID":
                                response = self.codex.grappler.getProcessID()
                            elif data["command"] == "Grappler.getBaseAddress":
                                response = self.codex.grappler.getBaseAddress()
                            else:
                                response = "Unknown command"
                        except Exception as e:
                            continue

                        # For demonstration, just echo back the command
                        response = f"{response}"

                        # Send response back to the client
                        client_socket.send(response.encode())
                except KeyboardInterrupt:
                    self.stop()

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print("Server is shutting down.")
        self.socket.close()
        sys.exit(0)
