from core.singleton import singleton
from core.grappler import Grappler
from core.memory import Memory
from core.communicator import Communicator
from modules.game import Game
from modules.player import Player


@singleton
class Codex:
    def __init__(self, process_name):
        super().__init__()
        # Initialize Grappler
        self.grappler = Grappler(self)

        # Attach Grappler to running Process
        self.grappler.attachTo(process_name)

        # Initialize Modules
        self.memory = Memory(self)
        self.communicator = Communicator(self)
        self.player = Player(self)
        self.game = Game(self)
