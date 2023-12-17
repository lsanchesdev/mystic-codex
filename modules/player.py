# Imports
import constants.memory as MemoryBook
import pprint
import sys


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
        self.pets = None

    def dump(self, format=True, stop_execution=False):
        if format:
            for attr, value in self.__dict__.items():
                print(f"{attr} ({type(value).__name__}):")
                pprint.pprint(value, indent=4)
                print()  # Add a blank line for better readability
        else:
            for attr, value in self.__dict__.items():
                print(f"{attr} = {value}")

        if stop_execution:
            sys.exit()

    def update(self):
        (self.name,) = self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_NAME, 16),
        (self.nickname,) = self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_NICKNAME, 16),
        (self.reputation,) = self.codex.gatekeeper.readFromBase(MemoryBook.MEMORY_USER_REPUTATION, 4),
        self.cash = {
            'pocket': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_CASH_POCKET, 4),
            'bank': None
        }
        self.experience = {
            'current': self.codex.gatekeeper.readFromBase(MemoryBook.MEMORY_USER_EXPERIENCE_CURRENT, 4),
            'max': None,
            'remaining': None,
        }
        self.stats = {
            'level': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_STATS_LEVEL_CURRENT, 2),
            'life': {
                'current': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_STATS_LIFE_CURRENT, 2),
                'max': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_STATS_LIFE_MAX, 2)
            },
            'mana': {
                'current': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_STATS_MANA_CURRENT, 2),
                'max': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_STATS_MANA_MAX, 2),
            },
            'attack': None,
            'defense': None,
            'dexterity': None,
            'anti-poison': None,
            'anti-hypnotism': None,
            'CR': None,
            'SR': None,
            'wuxing': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_STATS_WUXING, 2),
            'pet_raising': self.codex.gatekeeper.readFromBase(MemoryBook.MEMORY_USER_STATS_PET_RAISING, 2),
        }
        self.points = {
            'life': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POINTS_LIFE, 2),
            'mana': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POINTS_MANA, 2),
            'attack': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POINTS_ATTACK, 2),
            'defense': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POINTS_DEFENSE, 2),
            'dexterity': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POINTS_DEXTERITY, 2),
            'remaining': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POINTS_REMAINING, 2),
        }
        self.position = {
            'map': {
                'id': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POSITION_MAP_ID, 4),
                'name': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POSITION_MAP_NAME, 16),
            },
            'real': {
                "X": self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POSITION_REAL_X, 2),
                "Y": self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POSITION_REAL_Y, 2),
            },
            'relative': {
                "X": self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POSITION_RELATIVE_X, 2),
                "Y": self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_POSITION_RELATIVE_Y, 2),
            }
        }
        self.inventory = {
            'count': self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_INVENTORY_BAG_COUNT, 2),
            'bag': [],
            'equipped': [],
        }
        self.rank = {
            'id': None,
            'text': None,
            'type': None,
        }
        self.pets = {
            'count': self.codex.gatekeeper.read(MemoryBook.MEMORY_PETS_COUNT, 2),
            'marching': None,
            'list': [],
        }
        self.setRank()
        self.setInventory()
        self.calculateHumanAttributes()
        self.calculateExperience()
        self.setPets()

    def setPets(self):
        # Go through all pets
        for i in range(0, self.pets['count']):
            # Get memory address for pet
            list_pet = self.codex.gatekeeper.readList(i, MemoryBook.MEMORY_PETS,
                                                   MemoryBook.MEMORY_PETS_FIRST_PET)

            # Get memory address for equipped item
            equipped_item = self.codex.gatekeeper.read(list_pet + 0xB4, 4, True)

            # Extract pet information
            pet = {
                "id": self.codex.gatekeeper.read(list_pet + 0x90, 4),
                "name": self.codex.gatekeeper.read(list_pet + 4, 16),
                "level": self.codex.gatekeeper.read(list_pet + 0x38, 2),
                "loyal": self.codex.gatekeeper.read(list_pet + 0x94, 2),
                "is_marching": bool(self.codex.gatekeeper.read(list_pet + 0xB0, 2)),
                "experience": {
                    "current": self.codex.gatekeeper.read(list_pet + 0x3C, 4),
                    "max": 0
                },
                "stats": {
                    "life": {
                        "current": self.codex.gatekeeper.read(list_pet + 0x40, 4),
                        "max": self.codex.gatekeeper.read(list_pet + 0x44, 4),
                    },
                    "attack": self.codex.gatekeeper.read(list_pet + 0x1C, 4),
                    "defense": self.codex.gatekeeper.read(list_pet + 0x20, 4),
                    "dexterity": self.codex.gatekeeper.read(list_pet + 0x24, 4),
                    "without-item": {
                        "life": self.codex.gatekeeper.read(list_pet + 0x44, 4),
                        "attack": self.codex.gatekeeper.read(list_pet + 0x1C, 4),
                        "defense": self.codex.gatekeeper.read(list_pet + 0x20, 4),
                        "dexterity": self.codex.gatekeeper.read(list_pet + 0x24, 4),
                    }
                },
                "item": None,
                "medals": {
                    "attack": self.codex.gatekeeper.read(list_pet + 0x84, 4),
                    "defense": self.codex.gatekeeper.read(list_pet + 0x88, 4),
                    "dexterity": self.codex.gatekeeper.read(list_pet + 0x8C, 4),
                },
                "growth": {
                    "life": 0,
                    "3A": {
                        "attack": 0,
                        "defense": 0,
                        "dexterity": 0,
                        "total": 0,
                    }
                }
            }

            # Calculate Max Experience (Next Level Requirement)
            (pet['experience']['max'],) = int((pet["level"] + 1) * pet["level"] * 0.75),

            # Get equipped item attributes
            if equipped_item:
                pet['item'] = {
                    "id": self.codex.gatekeeper.read(equipped_item + 32, 4),
                    "type": self.codex.gatekeeper.read(equipped_item + 42, 2),
                    "name": self.codex.gatekeeper.read(equipped_item, 16),
                    "level": self.codex.gatekeeper.read(equipped_item + 44, 4),
                    "price": self.codex.gatekeeper.read(equipped_item + 36, 4),
                    "maker": self.codex.gatekeeper.read(equipped_item + 16, 16),
                    "stats": {
                        "life": self.codex.gatekeeper.read(equipped_item + 48, 2),
                        "mana": self.codex.gatekeeper.read(equipped_item + 50, 2),
                        "attack": self.codex.gatekeeper.read(equipped_item + 52, 2),
                        "defense": self.codex.gatekeeper.read(equipped_item + 54, 2),
                        "dexterity": self.codex.gatekeeper.read(equipped_item + 56, 2),
                        "anti-poison": self.codex.gatekeeper.read(equipped_item + 58, 2),
                        "CR": self.codex.gatekeeper.read(equipped_item + 60, 2),
                        "anti-hypnotism": self.codex.gatekeeper.read(equipped_item + 62, 2),
                        "SR": self.codex.gatekeeper.read(equipped_item + 64, 2),
                    }
                }

                # For each possible attribute bonus, remove it from the total
                for attr in pet['item']['stats']:
                    if pet['item']['stats'][attr]:
                        pet['stats']['without-item'][attr] -= pet['item']['stats'][attr]

            # Set calculation level
            if pet['level'] > 1:
                calculation_level = pet['level'] - 1
            else:
                calculation_level = 1

            # Calculate Growth (Life)
            pet['growth']['life'] = round(float(pet['stats']['without-item']['life']) / calculation_level, 2)

            # Sum attributes to calculate growth
            attributes = float(pet['stats']['without-item']['attack'] + pet['stats']['without-item']['defense'] + pet['stats']['without-item']['dexterity'])

            # Calculate Growth (3-A:Attack)
            pet['growth']['3A']['attack'] = round(((pet['stats']['without-item']['attack'] / (attributes * 100)) * 100) * 100, 2)
            pet['growth']['3A']['defense'] = round(((pet['stats']['without-item']['defense'] / (attributes * 100)) * 100) * 100, 2)
            pet['growth']['3A']['dexterity'] = round(((pet['stats']['without-item']['dexterity'] / (attributes * 100)) * 100) * 100, 2)
            pet['growth']['3A']['total'] = round(attributes / calculation_level, 2)

            # Push pet to list of pets
            self.pets['list'].append(pet)

            # In case of marching pet, set it
            if pet['is_marching']:
                self.pets['marching'] = pet

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
        # Go through all equipped items
        for i in range(0, len(MemoryBook.MEMORY_USER_INVENTORY_EQUIPPED)):
            try:
                # Get the memory address for equipped item
                list_item = self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_INVENTORY_EQUIPPED[i], is_pointer=True)

                # Extract item information
                item = {
                    "id": self.codex.gatekeeper.read(list_item + 32, 4),
                    "type": self.codex.gatekeeper.read(list_item + 42, 2),
                    "name": self.codex.gatekeeper.read(list_item, 16),
                    "level": self.codex.gatekeeper.read(list_item + 44, 4),
                    "price": self.codex.gatekeeper.read(list_item + 36, 4),
                    "maker": self.codex.gatekeeper.read(list_item + 16, 16),
                    "stats": {
                        "life": self.codex.gatekeeper.read(list_item + 48, 2),
                        "mana": self.codex.gatekeeper.read(list_item + 50, 2),
                        "attack": self.codex.gatekeeper.read(list_item + 52, 2),
                        "defense": self.codex.gatekeeper.read(list_item + 54, 2),
                        "dexterity": self.codex.gatekeeper.read(list_item + 56, 2),
                        "anti-poison": self.codex.gatekeeper.read(list_item + 58, 2),
                        "CR": self.codex.gatekeeper.read(list_item + 60, 2),
                        "anti-hypnotism": self.codex.gatekeeper.read(list_item + 62, 2),
                        "SR": self.codex.gatekeeper.read(list_item + 64, 2),
                    }
                }

                # Handle item type 600
                if item["type"] == 600:
                    item["stats"]["life"] = -item["stats"]["life"]

                # Push item to list of equipped items
                self.inventory['equipped'].append(item)
            except Exception as e:  # If there's no item equipped on that slot, move on.
                continue

    def setInventoryBag(self):
        # Go through all items in the inventory bag
        for i in range(0, int(self.inventory['count'])):
            # Get memory address for item
            list_item = self.codex.gatekeeper.readList(i, MemoryBook.MEMORY_USER_INVENTORY_BAG,
                                                   MemoryBook.MEMORY_USER_INVENTORY_BAG_FIRST_ITEM)
            list_item = int(list_item)

            # Extract item information
            item = {
                "id": self.codex.gatekeeper.read(list_item + 32, 4),
                "type": self.codex.gatekeeper.read(list_item + 42, 2),
                "name": self.codex.gatekeeper.read(list_item, 16),
                "level": self.codex.gatekeeper.read(list_item + 44, 4),
                "price": self.codex.gatekeeper.read(list_item + 36, 4),
                "maker": self.codex.gatekeeper.read(list_item + 16, 16),
                "stats": {
                    "life": self.codex.gatekeeper.read(list_item + 48, 2),
                    "mana": self.codex.gatekeeper.read(list_item + 50, 2),
                    "attack": self.codex.gatekeeper.read(list_item + 52, 2),
                    "defense": self.codex.gatekeeper.read(list_item + 54, 2),
                    "dexterity": self.codex.gatekeeper.read(list_item + 56, 2),
                    "anti-poison": self.codex.gatekeeper.read(list_item + 58, 2),
                    "CR": self.codex.gatekeeper.read(list_item + 60, 2),
                    "anti-hypnotism": self.codex.gatekeeper.read(list_item + 62, 2),
                    "SR": self.codex.gatekeeper.read(list_item + 64, 2),
                }
            }

            # Handle item type 600
            if item["type"] == 600:
                item["stats"]["life"] = -item["stats"]["life"]

            # Push item to list of items in the bag
            self.inventory['bag'].append(item)

    def setRank(self):
        (self.rank['id'],) = self.codex.gatekeeper.read(MemoryBook.MEMORY_USER_RANK, 2),
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
