from core.communicator import Communicator
from core.gatekeeper import Gatekeeper
from core.memory import Memory
from enums.grappler_type import GrapplerType
from modules.game import Game
from modules.player import Player
import os, sys, time


class NormalBehavior:

    def __init__(self, codex):
        super().__init__()
        self.codex = codex

    def update(self):
        self.codex.player.update()
        self.codex.game.update()
        self.codex.game.battle.update()

    def run(self):
        # Attach Grappler to running Process
        self.codex.grappler.attachTo(self.codex.parameters, GrapplerType.PROCESS)

        # Initialize Modules
        self.codex.memory = Memory(self.codex)
        self.codex.gatekeeper = Gatekeeper(self.codex)
        self.codex.communicator = Communicator(self.codex)
        self.codex.player = Player(self.codex)
        self.codex.game = Game(self.codex)

        # Run main loop
        self.main()

    def main(self):
        # Keep updating
        while True:
            # Debug
            print("Process ID:", self.codex.grappler.getProcessID())
            print("Process Base Memory Address:", self.codex.grappler.getBaseAddress())
            print()

            # Update necessary information
            self.update()

            # Dump player information on console
            # self.codex.player.dump(format=False)

            # self.codex.game.battle.enableSpeed()

            # Wait a cycle
            time.sleep(0.5)

            # Clear console
            os.system('cls')
