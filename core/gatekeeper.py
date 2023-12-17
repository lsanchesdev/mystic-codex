from enums.app_mode import AppMode
import json


class Gatekeeper:
    def __init__(self, codex):
        self.codex = codex
        self.process = {
            'id': codex.grappler.getProcessID(),
            'base_memory': codex.grappler.getBaseAddress()
        }
        self.client = {
            'socket': None,
            'connection': None,
        }

    def readFromBase(self, address, size, is_pointer=False):
        if self.codex.mode == AppMode.CLIENT:
            command = {
                'command': 'Memory.readFromBase',
                'address': address,
                'size': size,
                'is_pointer': is_pointer
            }
            return self.readFromSocket(json.dumps(command))
        else:
            return self.codex.memory.readFromBase(address, size, is_pointer)

    def read(self, address, size=4, is_pointer=False):
        if self.codex.mode == AppMode.CLIENT:
            command = {
                'command': 'Memory.read',
                'address': address,
                'size': size
            }
            return self.readFromSocket(json.dumps(command))
        else:
            return self.codex.memory.read(address, size, is_pointer)

    def write(self, address, data, size):
        if self.codex.mode == AppMode.CLIENT:
            pass
        else:
            return self.codex.memory.write(address, data, size)

    def readList(self, index, base_address, first_element_address):
        if self.codex.mode == AppMode.CLIENT:
            command = {
                'command': 'Memory.readList',
                'base_address': base_address,
                'first_element_address': first_element_address
            }
            return self.readFromSocket(json.dumps(command))
        else:
            return self.codex.memory.readList(index, base_address, first_element_address)

    def readFromSocket(self, command):
        # Send command to the server
        self.client['socket'].send(command.encode())

        # Receive and print the response
        return self.client['socket'].recv(1024).decode()