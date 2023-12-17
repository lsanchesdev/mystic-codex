#!/usr/bin/env python3
import sys

# Imports
from core.codex import Codex
from enums.app_mode import AppMode
from core.behavior.normal import NormalBehavior
from core.behavior.client import ClientBehavior
from core.behavior.server import ServerBehavior
from core.behavior.behavior import Behavior

# Define constants
PROCESS_NAME = "Monster&Me"
SERVER = {
    # 'ip': '185.62.56.218',
    'ip': 'localhost',
    'port': 8080
}

# Initialize Global Variables
codex = None
args = None


class MysticCodex:
    def __init__(self):
        self.behavior = Behavior(self)

        # Handle console arguments to decide which behavior to take
        self.behavior.check()

        # Initialize Codex
        self.codex = Codex({
            'process': PROCESS_NAME,
            'server': SERVER
        }, self.behavior.running_mode)

    def run(self):
        # Initialize Behavior
        if self.behavior.running_mode == AppMode.CLIENT:
            application = ClientBehavior(self.codex)
        elif self.behavior.running_mode == AppMode.SERVER:
            application = ServerBehavior(self.codex)
        else:
            application = NormalBehavior(self.codex)

        # Run application with selected behavior
        application.run()


if __name__ == "__main__":
    app = MysticCodex()
    app.run()
