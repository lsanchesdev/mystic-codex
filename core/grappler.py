from enums.grappler_type import GrapplerType
import constants.error as error
import socket
import sys
import win32gui
import win32process
import win32api
import win32con


class Grappler:

    def __init__(self, codex):
        super().__init__()
        self.codex = codex
        self.process = {
            'id': None,
            'handle': None
        }
        self.socket = None
        self.mode = None

    def attachTo(self, parameters, grappler_type=GrapplerType.PROCESS):
        self.mode = grappler_type
        if grappler_type == GrapplerType.SERVER:
            self.attachToServer(parameters)
        else:
            self.attachToProcess(parameters)

    def attachToProcess(self, parameters):
        # Find Process by Name and Extract Process ID
        self.findProcess(parameters['process'])

        # Exit otherwise
        if self.process['id'] is None:
            sys.exit(error.ERROR_PROCESS_ID_NOT_FOUND)

        # Open Process with Necessary Privileges
        self.process['handle'] = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, self.process['id'])

    def attachToServer(self, parameters):
        # Initialize
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        self.socket.connect((parameters['ip'], parameters['port']))

    def findProcess(self, name):
        # Find Window/Process with the given name
        processFinder = win32gui.FindWindow(None, name)

        # If process is found, extract Process ID from it
        if processFinder:
            _, self.process['id'] = win32process.GetWindowThreadProcessId(processFinder)

    def getMode(self):
        return self.mode

    def getProcessID(self):
        return self.process['id']

    def getBaseAddress(self):
        if self.process['handle']:
            modules = win32process.EnumProcessModules(self.process['handle'])
            base_address = modules[0]  # The first module is usually the main executable
            return base_address  # Convert to hexadecimal
        else:
            return None

    def getProcessHandle(self):
        return self.process['handle']
