import copy

class ItemManager:
    def __init__(self):
        self.buckets = {
            "Simple": [], "Martial": [], 
            "Light": [], "Medium": [], "Heavy": [], "Shield": [],
            "Main": [], "Off": [], "Melee": [], "Ranged": []
        }
        self._populate()

    def _populate(self):
        for cls in Item.registry:
            for c in cls.cat:
                self.buckets[c].append(cls.base_name)

    def get_list(self, category):
        return self.buckets.get(category, [])

    def create(self, name, tier=0):
        for cls in Item.registry:
            if cls.base_name == name:
                return cls(tier)
        return None

class Item:
    registry = []
    
    base_name = ""
    cat = set()
    prop = set()
    cost = 0
    weight = 0
    
    Attune = False

    def __init__(self, tier=0):
        self.tier = tier

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Item.registry.append(cls)

    @property
    def id(self):
        return f"{self.base_name}_{self.tier}"

class Weapon(Item):
    dType = ""
    Range = ""
    Roll = ""
    sDam = 1

    @property
    def Hit(self):
        return self.tier

    @property
    def Dam(self):
        return self.tier * self.sDam

class Armor(Item):
    bAC = 0
    sDis = False
    sReq = 0
    dMax = 0

    @property
    def AC(self):
        return self.bAC + self.tier

class Dagger(Weapon):
    base_name = "Dagger"
    cat = {"Simple", "Melee", "Main", "Off"}
    prop = {"Finesse", "Light", "Thrown", "Range"}
    dType = "Piercing"
    Range = "5 - 20/60 ft"
    Roll = "1d4"
    cost = 2
    weight = 1

class Greatsword(Weapon):
    base_name = "Greatsword"
    cat = {"Martial", "Melee", "Main"}
    prop = {"Heavy", "Two-Handed"}
    dType = "Slashing"
    Range = "5 ft"
    Roll = "2d6"
    cost = 50
    weight = 6

class Lance(Weapon):
    base_name = "Lance"
    cat = {"Martial", "Melee", "Main"}
    prop = {"Reach", "Lance"}
    dType = "Piercing"
    Range = "10 ft"
    Roll = "1d12"
    cost = 10
    weight = 6

class Net(Weapon):
    base_name = "Net"
    cat = {"Martial", "Ranged", "Main", "Off"}
    prop = {"Thrown", "Range", "Net"}
    dType = "" 
    Range = "5/15 ft"
    Roll = ""
    sDam = 0
    cost = 1
    weight = 3

class Shield(Armor):
    base_name = "Shield"
    cat = {"Shield", "Off"}
    bAC = 2
    dMax = 100
    cost = 10
    weight = 6

class Plate(Armor):
    base_name = "Plate"
    cat = {"Heavy"}
    bAC = 18
    sDis = True
    sReq = 15
    dMax = 0
    cost = 1500
    weight = 65