from core.communicator import Communicator
from core.gatekeeper import Gatekeeper
import constants.memory as MemoryBook
import socket, time, os

from modules.game import Game
from modules.player import Player


class ClientBehavior:

    def __init__(self, codex):
        super().__init__()
        self.codex = codex
        self.codex.gatekeeper = Gatekeeper(self.codex)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        self.run()

    def run(self):
        self.connection = self.socket.connect((self.codex.parameters['server']['ip'], self.codex.parameters['server']['port']))
        self.codex.gatekeeper.client = {
            'socket': self.socket,
            'connection': self.connection
        }
        self.codex.communicator = Communicator(self.codex)
        self.codex.player = Player(self.codex)
        self.codex.game = Game(self.codex)
        self.main()

    def main(self):
        while True:
            # Debug
            print("Process ID:", self.codex.grappler.getProcessID())
            print("Process Base Memory Address:", self.codex.grappler.getBaseAddress())
            print()

            # Update
            self.update()

            self.codex.player.dump() 

            # Wait a cycle
            time.sleep(1)

            # Clear console
            os.system('cls')

    def update(self):
        self.codex.player.update()
        self.codex.game.update()
        self.codex.game.battle.update()