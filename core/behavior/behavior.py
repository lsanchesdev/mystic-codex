from enums.app_mode import AppMode
import argparse


class Behavior:

    def __init__(self, codex):
        super().__init__()
        self.codex = codex
        self.modes = None
        self.running_mode = None

    def check(self):
        # Decide in which mode the codex will run
        parser = argparse.ArgumentParser(description="Run the script in client or server mode.")
        parser.add_argument('--client', action='store_true', help='Run in client mode')
        parser.add_argument('--server', action='store_true', help='Run in server mode')

        # Pre-parse arguments
        args = parser.parse_args()

        # If not running on any particular mode, run it in normal mode
        if args.client is False and args.server is False:
            parser.add_argument('--normal', action='store_false', help='Run in normal mode')
        else:
            parser.add_argument('--normal', action='store_true', help='Run in normal mode')

        # Parse arguments
        self.modes = parser.parse_args()

        # Choose in which mode to run the application
        if self.modes.client:
            self.running_mode = AppMode.CLIENT
        elif self.modes.server:
            self.running_mode = AppMode.SERVER
        else:
            self.running_mode = AppMode.NORMAL
