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
    # player.update()
    pass


def main():
    # Initialize Application
    initialize()

    # Debug
    print("Process ID:", codex.grappler.getProcessID())
    print("Process Base Memory Address:", codex.grappler.getBaseAddress())

    # Keep updating
    while True:
        codex.player.update()

        print(codex.player.dump(format=False))

        import time, os
        time.sleep(1)

        os.system('cls')


if __name__ == "__main__":
    main()
