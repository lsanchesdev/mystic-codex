import constants.error as error
import win32gui
import win32process
import win32api
import win32con
import sys


class Grappler:

    def __init__(self, codex):
        super().__init__()
        self.codex = codex
        self.process_id = None
        self.process_handle = None

    def attachTo(self, name):
        # Find Process by Name and Extract Process ID
        self.findProcess(name)

        # Exit otherwise
        if self.process_id is None:
            sys.exit(error.ERROR_PROCESS_ID_NOT_FOUND)

        # Open Process with Necessary Privileges
        self.process_handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, self.process_id)

    def findProcess(self, name):
        # Find Window/Process with the given name
        processFinder = win32gui.FindWindow(None, name)

        # If process is found, extract Process ID from it
        if processFinder:
            _, self.process_id = win32process.GetWindowThreadProcessId(processFinder)

    def getProcessID(self):
        return self.process_id

    def getBaseAddress(self):
        if self.process_handle:
            modules = win32process.EnumProcessModules(self.process_handle)
            base_address = modules[0]  # The first module is usually the main executable
            return base_address  # Convert to hexadecimal
        else:
            return None

    def getProcessHandle(self):
        return self.process_handle
