# Imports
import constants.memory as MemoryBook
import pprint


class Player:

    def __init__(self, codex):
        super().__init__()
        self.codex = codex
        self.name = None
        self.nickname = None
        self.reputation = None
        self.cash = None
        self.experience = None
        self.stats = None
        self.points = None
        self.position = None
        self.inventory = None
        self.rank = None

    def dump(self, format=True, stop_execution=True):
        if format:
            for attr, value in self.__dict__.items():
                print(f"{attr} ({type(value).__name__}):")
                pprint.pprint(value, indent=4)
                print()  # Add a blank line for better readability
        else:
            for attr, value in self.__dict__.items():
                print(f"{attr} = {value}")

        if stop_execution:
            exit()

    def update(self):
        (self.name,) = self.codex.memory.read(MemoryBook.MEMORY_USER_NAME, 16),
        (self.nickname,) = self.codex.memory.read(MemoryBook.MEMORY_USER_NICKNAME, 16),
        (self.reputation,) = self.codex.memory.readFromBase(MemoryBook.MEMORY_USER_REPUTATION, 4),
        self.cash = {
            'pocket': self.codex.memory.read(MemoryBook.MEMORY_USER_CASH_POCKET, 4),
            'bank': None
        }
        self.experience = {
            'current': self.codex.memory.readFromBase(MemoryBook.MEMORY_USER_EXPERIENCE_CURRENT, 4),
            'max': None,
            'remaining': None,
        }
        self.stats = {
            'level': self.codex.memory.read(MemoryBook.MEMORY_USER_STATS_LEVEL_CURRENT, 2),
            'life': {
                'current': self.codex.memory.read(MemoryBook.MEMORY_USER_STATS_LIFE_CURRENT, 2),
                'max': self.codex.memory.read(MemoryBook.MEMORY_USER_STATS_LIFE_MAX, 2)
            },
            'mana': {
                'current': self.codex.memory.read(MemoryBook.MEMORY_USER_STATS_MANA_CURRENT, 2),
                'max': self.codex.memory.read(MemoryBook.MEMORY_USER_STATS_MANA_MAX, 2),
            },
            'attack': None,
            'defense': None,
            'dexterity': None,
            'anti-poison': None,
            'anti-hypnotism': None,
            'CR': None,
            'SR': None,
            'wuxing': self.codex.memory.read(MemoryBook.MEMORY_USER_STATS_WUXING, 2),
            'pet_raising': self.codex.memory.readFromBase(MemoryBook.MEMORY_USER_STATS_PET_RAISING, 2),
        }
        self.points = {
            'life': self.codex.memory.read(MemoryBook.MEMORY_USER_POINTS_LIFE, 2),
            'mana': self.codex.memory.read(MemoryBook.MEMORY_USER_POINTS_MANA, 2),
            'attack': self.codex.memory.read(MemoryBook.MEMORY_USER_POINTS_ATTACK, 2),
            'defense': self.codex.memory.read(MemoryBook.MEMORY_USER_POINTS_DEFENSE, 2),
            'dexterity': self.codex.memory.read(MemoryBook.MEMORY_USER_POINTS_DEXTERITY, 2),
            'remaining': self.codex.memory.read(MemoryBook.MEMORY_USER_POINTS_REMAINING, 2),
        }
        self.position = {
            'map': {
                'id': self.codex.memory.read(MemoryBook.MEMORY_USER_POSITION_MAP_ID, 4),
                'name': self.codex.memory.read(MemoryBook.MEMORY_USER_POSITION_MAP_NAME, 16),
            },
            'real': {
                "X": self.codex.memory.read(MemoryBook.MEMORY_USER_POSITION_REAL_X, 2),
                "Y": self.codex.memory.read(MemoryBook.MEMORY_USER_POSITION_REAL_Y, 2),
            },
            'relative': {
                "X": self.codex.memory.read(MemoryBook.MEMORY_USER_POSITION_RELATIVE_X, 2),
                "Y": self.codex.memory.read(MemoryBook.MEMORY_USER_POSITION_RELATIVE_Y, 2),
            }
        }
        self.inventory = {
            'count': self.codex.memory.read(MemoryBook.MEMORY_USER_INVENTORY_BAG_COUNT, 2),
            'bag': [],
            'equipped': [],
        }
        self.rank = {
            'id': None,
            'text': None,
            'type': None,
        }
        self.setRank()
        self.setInventory()
        self.calculateHumanAttributes()
        self.calculateExperience()

    def calculateExperience(self):
        self.experience['max'] = self.stats['level'] * (self.stats['level'] + 1)
        self.experience['remaining'] = self.experience['max'] - self.experience['current']

    def calculateHumanAttributes(self):
        # Set an empty array for the calculated attributes
        calculated = {
            'attack': 0,
            'defense': 0,
            'dexterity': 0,
            'anti-poison': 0,
            'anti-hypnotism': 0,
            'CR': 0,
            'SR': 0,
        }

        # Sum attributes already distributed
        calculated['attack'] += self.points['attack']
        calculated['defense'] += self.points['defense']
        calculated['dexterity'] += self.points['dexterity']

        # Sum attributes from items
        for item in self.inventory["equipped"]:
            calculated['attack'] += item['stats']['attack']
            calculated['defense'] += item['stats']['defense']
            calculated['dexterity'] += item['stats']['dexterity']
            calculated['anti-poison'] += item['stats']['anti-poison']
            calculated['anti-hypnotism'] += item['stats']['anti-hypnotism']
            calculated['CR'] += item['stats']['CR']
            calculated['SR'] += item['stats']['SR']

        # Push calculated attributes back to the human stats
        self.stats['attack'] = calculated['attack']
        self.stats['defense'] = calculated['defense']
        self.stats['dexterity'] = calculated['dexterity']
        self.stats['anti-poison'] = calculated['anti-poison']
        self.stats['anti-hypnotism'] = calculated['anti-hypnotism']
        self.stats['CR'] = calculated['CR']
        self.stats['SR'] = calculated['SR']

    def setInventory(self):
        self.setInventoryBag()
        self.setInventoryEquipped()

    def setInventoryEquipped(self):
        list_item = 0x6BD0D4
        data = self.codex.memory.read(0x6BD0D4, is_pointer=True)

        print(data)
        for i in range(0, len(MemoryBook.MEMORY_USER_INVENTORY_EQUIPPED)):
            try:
                list_item = self.codex.memory.read(MemoryBook.MEMORY_USER_INVENTORY_EQUIPPED[i], is_pointer=True)

                item = {
                    "id": self.codex.memory.read(list_item + 32, 4),
                    "type": self.codex.memory.read(list_item + 42, 2),
                    "name": self.codex.memory.read(list_item, 16),
                    "level": self.codex.memory.read(list_item + 44, 4),
                    "price": self.codex.memory.read(list_item + 36, 4),
                    "maker": self.codex.memory.read(list_item + 16, 16),
                    "stats": {
                        "life": self.codex.memory.read(list_item + 48, 2),
                        "mana": self.codex.memory.read(list_item + 50, 2),
                        "attack": self.codex.memory.read(list_item + 52, 2),
                        "defense": self.codex.memory.read(list_item + 54, 2),
                        "dexterity": self.codex.memory.read(list_item + 56, 2),
                        "anti-poison": self.codex.memory.read(list_item + 58, 2),
                        "CR": self.codex.memory.read(list_item + 60, 2),
                        "anti-hypnotism": self.codex.memory.read(list_item + 62, 2),
                        "SR": self.codex.memory.read(list_item + 64, 2),
                    }
                }

                if item["type"] == 600:
                    item["stats"]["life"] = -item["stats"]["life"]

                self.inventory['equipped'].append(item)
            except Exception as e:
                continue

    def setInventoryBag(self):
        for i in range(0, self.inventory['count']):
            list_item = self.codex.memory.readList(i, MemoryBook.MEMORY_USER_INVENTORY_BAG,
                                                   MemoryBook.MEMORY_USER_INVENTORY_BAG_FIRST_ITEM)

            item = {
                "id": self.codex.memory.read(list_item + 32, 4),
                "type": self.codex.memory.read(list_item + 42, 2),
                "name": self.codex.memory.read(list_item, 16),
                "level": self.codex.memory.read(list_item + 44, 4),
                "price": self.codex.memory.read(list_item + 36, 4),
                "maker": self.codex.memory.read(list_item + 16, 16),
                "stats": {
                    "life": self.codex.memory.read(list_item + 48, 2),
                    "mana": self.codex.memory.read(list_item + 50, 2),
                    "attack": self.codex.memory.read(list_item + 52, 2),
                    "defense": self.codex.memory.read(list_item + 54, 2),
                    "dexterity": self.codex.memory.read(list_item + 56, 2),
                    "anti-poison": self.codex.memory.read(list_item + 58, 2),
                    "CR": self.codex.memory.read(list_item + 60, 2),
                    "anti-hypnotism": self.codex.memory.read(list_item + 62, 2),
                    "SR": self.codex.memory.read(list_item + 64, 2),
                }
            }

            if item["type"] == 600:
                item["stats"]["life"] = -item["stats"]["life"]

            self.inventory['bag'].append(item)

    def setRank(self):
        (self.rank['id'],) = self.codex.memory.read(MemoryBook.MEMORY_USER_RANK, 2),
        self.rank['text'] = self.getRankText(self.rank['id'])
        self.rank['type'] = self.getRankType(self.rank['id'])

    def getRankType(self, rank):
        if rank == 0:
            return "Mortal"
        elif rank == 1:
            return "Basic God"
        elif rank == 2:
            return "Junior [...]"
        elif rank == 3:
            return "Senior [...]"
        elif rank == 4:
            return "Super [...]"
        elif rank == 5:
            return "Master [...]"

    def getRankText(self, rank):
        rank_text = ""

        if rank == 0:  # Mortal
            if self.stats['level'] > 1100:
                rank_text = "Senior Master"
            elif self.stats['level'] > 900:
                rank_text = "Junior Master"
            elif self.stats['level'] > 750:
                rank_text = "Senior Knight"
            elif self.stats['level'] > 500:
                rank_text = "Junior Knight"
            elif self.stats['level'] > 300:
                rank_text = "Basic Knight"
            elif self.stats['level'] > 150:
                rank_text = "Senior Warrior"
            elif self.stats['level'] > 50:
                rank_text = "Junior Warrior"
            else:
                rank_text = "Basic Warrior"
        elif rank == 1:
            rank_text = "Basic God"
        elif rank == 2:
            rank_text = "Junior [...]"
        elif rank == 3:
            rank_text = "Senior [...]"
        elif rank == 4:
            rank_text = "Super [...]"
        elif rank == 5:
            rank_text = "Master [...]"

        return rank_text
