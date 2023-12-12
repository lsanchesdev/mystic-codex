#!/usr/bin/env python3

# Imports
from core.codex import Codex

# Define constants
PROCESS_NAME = "Monster&Me"

# Initialize Global Variables
codex = None


def initialize():
    # Call Global Variables
    global codex

    # Initialize Modules
    codex = Codex(PROCESS_NAME)


def update():
    codex.player.update()


def main():
    # Initialize Application
    initialize()

    # Debug
    print("Process ID:", codex.grappler.getProcessID())
    print("Process Base Memory Address:", codex.grappler.getBaseAddress())

    # Keep updating
    while True:
        # Update necessary information
        update()

        # Dump player information on console
        print(codex.player.dump(format=False))

        # Wait 1 second
        import time, os
        time.sleep(1)

        # Clear console
        os.system('cls')


if __name__ == "__main__":
    main()
