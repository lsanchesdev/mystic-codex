#!/usr/bin/env python3
import constants.memory
# Imports
from core.codex import Codex
from core.communicator import Communicator
from modules.player import Player

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

    print("Process ID:", codex.grappler.getProcessID())
    print("Process Base Memory Address:", codex.grappler.getBaseAddress())

    codex.player.update()
    print(codex.player.experience)

    # while True:
    #     codex.player.update()
#
    #     print(codex.player.experience)
#
    #     import time, os
    #     time.sleep(1)
#
    #     os.system('cls')



    #print(codex.player.dump(format=False))

    #codex.game.beginBattle()

    # codex.memory.write(constants.memory.MEMORY_USER_POSITION_RELATIVE_X, 93, 4)
    # codex.memory.write(constants.memory.MEMORY_USER_POSITION_RELATIVE_Y, 49, 4)
    #codex.memory.write(constants.memory.MEMORY_USER_POSITION_RELATIVE_X, 82, 4)
    #codex.memory.write(constants.memory.MEMORY_USER_POSITION_RELATIVE_Y, 24, 4)
#
    # import time
    # time.sleep(1)

    # codex.game.closeWuxingOven()


if __name__ == "__main__":
    main()
