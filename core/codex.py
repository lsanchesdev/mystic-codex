from core.singleton import singleton
from core.grappler import Grappler
from core.grappler import GrapplerType
from core.memory import Memory
from core.communicator import Communicator
from modules.game import Game
from modules.player import Player


@singleton
class Codex:
    def __init__(self, parameters, mode=GrapplerType.PROCESS):
        super().__init__()

        # Store parameters
        self.parameters = parameters
        self.mode = mode

        # Initialize Grappler
        self.grappler = Grappler(self)

        # Initialize Modules
        self.memory = None
        self.communicator = None
        self.player = None
        self.game = None
