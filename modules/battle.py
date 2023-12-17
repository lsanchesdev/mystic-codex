import constants.game_actions as GameActionsBook
import constants.battle as BattleBook


class Battle:

    def __init__(self, codex):
        super().__init__()
        self.codex = codex
        self.is_at_battle = False
        self.enemy = {
            'count': 0,
            'dead': 0
        }

    def begin(self):
        self.codex.communicator.sendCommand(GameActionsBook.GAME_ACTION_BEGIN_BATTLE)

    def update(self):
        if self.codex.game.getState() == self.codex.game.state.BATTLE:
            self.is_at_battle = True
            self.enemy = {
                'count': self.codex.gatekeeper.readFromBase(BattleBook.BATTLE_ENEMY_TOTAL_COUNT, 4),
                'dead': self.codex.gatekeeper.readFromBase(BattleBook.BATTLE_ENEMY_DEAD_COUNT, 2),
            }
        else:
            self.enemy = {
                'count': 0,
                'dead': 0
            }

    def enableSpeed(self):
        self.enableSpeedAttack()
        self.enableSpeedMovement()
        self.enableSpeedCatch()

    def enableSpeedCatch(self):
        for item in BattleBook.BATTLE_SPEED_CATCH:
            self.codex.gatekeeper.write(item["address"], item["value"], item["size"])

    def enableSpeedAttack(self):
        for item in BattleBook.BATTLE_SPEED_ATTACK:
            self.codex.gatekeeper.write(item["address"], item["value"], item["size"])

    def enableSpeedMovement(self):
        for item in BattleBook.BATTLE_SPEED_MOVEMENT:
            self.codex.gatekeeper.write(item["address"], item["value"], item["size"])