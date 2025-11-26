from box import Box
import q 

def Resolve_Select(data, parent, Level, PB):
    if data["Options"][0] == "0_Wizard":
        data["Options"] = q.fTome(Level=0, Caster="Wizard")
    data["Choices"] = data["Choices"]


def Resolve_Breath(data, parent, Level, PB):
    usage = [0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4][Level]
    damage = [0, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5][Level]
    data["Use"] = [False] * usage
    data["Damage"] = damage

def Resolve_Use(data, parent, Level, PB):
    rule = data["Use"]

    if isinstance(rule, list):  count = rule[Level]
    elif isinstance(rule, int): count = rule
    elif isinstance(rule, str): 
        if rule == "PB":  count = PB

    else: count = 0
    data["Use"] = [False] * count

    if "lDesc" in data:
        valid = [int(l) for l in data["lDesc"] if int(l) <= Level]
        if valid: data["Desc"] = data["lDesc"][max(valid)]

def Resolve_HP(data, parent, Level, PB):
    val = Level if data["HP"] == "LEVEL" else 0
    parent.Combat.HP = val

def Resolve_Spell(data, parent, Level, PB):
    data["Spells"] = {}
    for spell in data["Given"].values():
        state = "Cantrip" if q.Grimoir[spell]["Level"] == 0 else False
        data["Spells"][spell] = state

def Resolve_Passive(data, parent, Level, PB):
    pass

Feature_Map = {
    "Breath_Weapon": Resolve_Breath,
    "Select": Resolve_Select,
    "HP": Resolve_HP,
    "Use": Resolve_Use,
    "Spell": Resolve_Spell,
    "Passive": Resolve_Passive 
}

class Race_Template:
    def __init__(self):
        self.Speed = Box({"Walk": 0, "Climb": 0, "Swim": 0, "Fly": 0, "Burrow": 0})
        self.Vision = Box({"Dark": 0, "Blind": 0, "Tremor": 0, "Tru": 0})
        self.Prof = Box({"Skill": [], "Weapon": [], "Armor": [], "Tool": [], "Lang": []})
        self.Combat = Box({"Initiative": 0, "HP": 0, "HD": 0})
        self.Features = [] 
        
    def add_feature(self, meta, Desc=None, **kwargs):
        name, level, tag = meta
        data = {"Name": name, "Level": level, "Tag": tag}
        if Desc: data["Desc"] = Desc
        data.update(kwargs)
        self.Features.append(data)

Dragonborn_map = {
    "Black":  ["Acid",      "Line", "DEX"],
    "Blue":   ["Lightning", "Line", "DEX"],
    "Brass":  ["Fire",      "Line", "DEX"],
    "Bronze": ["Lightning", "Line", "DEX"],
    "Copper": ["Acid",      "Line", "DEX"],
    "Gold":   ["Fire",      "Cone", "DEX"],
    "Green":  ["Poison",    "Cone", "CON"],
    "Red":    ["Fire",      "Cone", "DEX"],
    "Silver": ["Cold",      "Cone", "CON"],
    "White":  ["Cold",      "Cone", "CON"]
}

class Dragonborn(Race_Template):
    def __init__(self): 
        super().__init__()
        self.Speed.Walk = 30
        self.Prof.Lang = ["Common", "Draconic"]

    def _breath_weapon(self, spec):
        data = Dragonborn_map[spec]
        Type =  data[0]
        Shape = data[1]
        Save = data[2]
        return {"Name": "Breath Weapon","Level": 1,"Tag": "Breath_Weapon","Save": Save,"Damage": 0,"Use": 0,"Desc": [f"(Action) 30ft {Shape}, DC {{SV}} {Save} save. Fail: {{Damage}}d6 {Type}. Success: Half."]}
    
    def _resistance(self, spec):
        Type = Dragonborn_map[spec][0]
        return {"Name": "Draconic Resistance","Level": 1,"Tag": "Passive","Desc": [f"Resistance to {Type} damage."]}

class Dragonborn_Black(Dragonborn):
    def __init__(self): 
        super().__init__()
        self.Features.append(self._breath_weapon("Black"))
        self.Features.append(self._resistance("Black"))

class Dragonborn_Blue(Dragonborn):
    def __init__(self): 
        super().__init__()
        self.Features.append(self._breath_weapon("Blue"))
        self.Features.append(self._resistance("Blue"))

class Dragonborn_Brass(Dragonborn):
    def __init__(self): 
        super().__init__()
        self.Features.append(self._breath_weapon("Brass"))
        self.Features.append(self._resistance("Brass"))

class Dragonborn_Bronze(Dragonborn):
    def __init__(self): 
        super().__init__()
        self.Features.append(self._breath_weapon("Bronze"))
        self.Features.append(self._resistance("Bronze"))

class Dragonborn_Copper(Dragonborn):
    def __init__(self): 
        super().__init__()
        self.Features.append(self._breath_weapon("Copper"))
        self.Features.append(self._resistance("Copper"))

class Dragonborn_Gold(Dragonborn):
    def __init__(self): 
        super().__init__()
        self.Features.append(self._breath_weapon("Gold"))
        self.Features.append(self._resistance("Gold"))

class Dragonborn_Green(Dragonborn):
    def __init__(self): 
        super().__init__()
        self.Features.append(self._breath_weapon("Green"))
        self.Features.append(self._resistance("Green"))

class Dragonborn_Red(Dragonborn):
    def __init__(self): 
        super().__init__()
        self.Features.append(self._breath_weapon("Red"))
        self.Features.append(self._resistance("Red"))

class Dragonborn_Silver(Dragonborn):
    def __init__(self): 
        super().__init__()
        self.Features.append(self._breath_weapon("Silver"))
        self.Features.append(self._resistance("Silver"))

class Dragonborn_White(Dragonborn):
    def __init__(self): 
        super().__init__()
        self.Features.append(self._breath_weapon("White"))
        self.Features.append(self._resistance("White"))

class Dwarf(Race_Template):
    def __init__(self): 
        super().__init__()
        self.Speed.Walk = 25
        self.Vision.Dark = 60
        self.Prof.Lang = ["Common", "Dwarvish"]
        self.Prof.Weapon = ["Battleaxe", "Handaxe", "Light Hammer", "Warhammer"]
        self.add_feature(meta=["Dwarven Resilience", 1, "Passive"], Desc=["Advantage on Poison saves, Resistance to Poison damage."])
        self.add_feature(meta=["Stonecunning", 1, "Passive"], Desc=["Add 2PB to History checks on stonework."])

class Dwarf_Hill(Dwarf):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Dwarven Toughness", 1, "HP"], HP="LEVEL", Desc=["HP Max increases by 1 per level."])

class Dwarf_Mountain(Dwarf):
    def __init__(self): 
        super().__init__()
        self.Prof.Armor = ["Light", "Medium"]

class Elf(Race_Template):
    def __init__(self): 
        super().__init__()
        self.Speed.Walk = 30
        self.Vision.Dark = 60
        self.Prof.Skill = ["Perception"]
        self.Prof.Lang = ["Common", "Elvish"]
        self.add_feature(meta=["Fey Ancestry", 1, "Passive"], Desc=["Advantage vs Charm, Immune to magical sleep."])
        self.add_feature(meta=["Trance", 1, "Passive"], Desc=["Meditate 4 hours instead of sleep."])

class Elf_Drow(Elf):
    def __init__(self): 
        super().__init__()
        self.Vision.Dark = 120
        self.Prof.Weapon = ["Rapier", "Shortsword", "Hand Crossbow"]
        self.add_feature(meta=["Sunlight Sensitivity", 1, "Passive"], Desc=["Disadvantage on Attack/Perception in direct sunlight."])
        self.add_feature(meta=["Drow Magic", 1, "Spell"], Given={"1": "Dancing Lights", "3": "Faerie Fire", "5": "Darkness"})

class Elf_High(Elf):
    def __init__(self): 
        super().__init__()
        self.Prof.Weapon = ["Longsword", "Shortsword", "Shortbow", "Longbow"]
        self.add_feature(meta=["Cantrip", 1, "Select"], Options=["0_Wizard"], Choices=1)

class Elf_Shadar_Kai(Elf):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Necrotic Resistance", 1, "Passive"], Desc=["Resistance to Necrotic damage."])
        self.add_feature(meta=["Blessing of the Raven Queen", 1, "Use"], Use="PB", lDesc={1: ["(Bonus) Teleport 30ft."], 3: ["(Bonus) Teleport 30ft. Gain Resistance to all dmg until start of next turn."]})
class Elf_Wood(Elf):
    def __init__(self): 
        super().__init__()
        self.Speed.Walk = 35
        self.Prof.Weapon = ["Longsword", "Shortsword", "Shortbow", "Longbow"]
        self.add_feature(meta=["Mask of the Wild", 1, "Passive"], Desc=["Can hide in light obscuration (foliage, rain, etc)."])

class Empty(Race_Template):
    def __init__(self): super().__init__()

class Gnome(Race_Template):
    def __init__(self): 
        super().__init__()
        self.Speed.Walk = 25
        self.Vision.Dark = 60
        self.Prof.Lang = ["Common", "Gnomish"]
        self.add_feature(meta=["Gnome Cunning", 1, "Passive"], Desc=["Advantage on INT/WIS/CHA saves vs Magic."])

class Gnome_Forest(Gnome):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Natural Illusionist", 1, "Spell"], Given={"1": "Minor Illusion"})
        self.add_feature(meta=["Speak with Small Beasts", 1, "Passive"], Desc=["Communicate simple ideas with Small beasts."])

class Gnome_Rock(Gnome):
    def __init__(self): 
        super().__init__()
        self.Prof.Tool.append("Tinker's Tools")
        self.add_feature(meta=["Artificer's Lore", 1, "Passive"], Desc=["Add 2PB to History checks on magic/tech items."])
        self.add_feature(meta=["Tinker", 1, "Select"], Desc=["Construct Tiny clockwork device (1hr, 10gp, AC 5, 1hp). Lasts 24h. Max 3."], Choices=1, Options=["Clockwork Toy", "Fire Starter", "Music Box"], Multi_Desc={"Clockwork Toy": "Moves 5ft random direction, makes noise.", "Fire Starter": "Action to produce miniature flame.", "Music Box": "Plays single song."})

class Half_Orc(Race_Template):
    def __init__(self): 
        super().__init__()
        self.Speed.Walk = 30
        self.Vision.Dark = 60
        self.Prof.Skill = ["Intimidation"]
        self.Prof.Lang = ["Common", "Orc"]
        self.add_feature(meta=["Relentless Endurance", 1, "Passive"], Desc=["Drop to 1HP instead of 0HP once per Long Rest."])
        self.add_feature(meta=["Savage Attacks", 1, "Passive"], Desc=["Crit with melee weapon adds one extra damage die."])

class Half_Orc_Standard(Half_Orc):
    def __init__(self): super().__init__()

class Halfling(Race_Template):
    def __init__(self): 
        super().__init__()
        self.Speed.Walk = 25
        self.Prof.Lang = ["Common", "Halfling"]
        self.add_feature(meta=["Lucky", 1, "Passive"], Desc=["Reroll 1s on d20 (Attack/Check/Save). Must use new roll."])
        self.add_feature(meta=["Brave", 1, "Passive"], Desc=["Advantage on saves vs Frightened."])
        self.add_feature(meta=["Halfling Nimbleness", 1, "Passive"], Desc=["Move through space of creatures larger than you."])

class Halfling_Lightfoot(Halfling):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Naturally Stealthy", 1, "Passive"], Desc=["Hide when obscured by creature one size larger."])

class Halfling_Stout(Halfling):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Stout Resilience", 1, "Passive"], Desc=["Advantage on Poison saves, Resistance to Poison damage."])

class Harengon(Race_Template):
    def __init__(self): 
        super().__init__()
        self.Speed.Walk = 30
        self.Prof.Skill = ["Perception"]
        self.Prof.Lang = ["Common"]
        self.add_feature(meta=["Hare-Trigger", 1, "Passive"], Desc=["Add PB to Initiative."])
        self.add_feature(meta=["Lucky Footwork", 1, "Passive"], Desc=["(Reaction) On failed DEX save, add 1d4."])
        self.add_feature(meta=["Rabbit Hop", 1, "Use"], Use="PB", Desc=["(Bonus) Jump 5PB ft, no Opportunity Attacks."])

class Harengon_Standard(Harengon):
    def __init__(self): super().__init__()

class Human(Race_Template):
    def __init__(self): 
        super().__init__()
        self.Speed.Walk = 30
        self.Prof.Lang = ["Common"]

class Human_Standard(Human):
    def __init__(self): super().__init__()

class Tiefling(Race_Template):
    def __init__(self): 
        super().__init__()
        self.Speed.Walk = 30
        self.Vision.Dark = 60
        self.Prof.Lang = ["Common", "Infernal"]
        self.add_feature(meta=["Hellish Resistance", 1, "Passive"], Desc=["Resistance to Fire damage."])

class Tiefling_Asmodeus(Tiefling):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Infernal Legacy", 1, "Spell"], Given={"1": "Thaumaturgy", "3": "Hellish Rebuke", "5": "Darkness"})

class Tiefling_Baalzebul(Tiefling):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Legacy of Maladomini", 1, "Spell"], Given={"1": "Thaumaturgy", "3": "Ray of Sickness", "5": "Crown of Madness"})

class Tiefling_Dispater(Tiefling):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Legacy of Dis", 1, "Spell"], Given={"1": "Thaumaturgy", "3": "Disguise Self", "5": "Detect Thoughts"})

class Tiefling_Fierna(Tiefling):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Legacy of Phlegethos", 1, "Spell"], Given={"1": "Friends", "3": "Charm Person", "5": "Suggestion"})

class Tiefling_Glasya(Tiefling):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Legacy of Malbolge", 1, "Spell"], Given={"1": "Minor Illusion", "3": "Disguise Self", "5": "Invisibility"})

class Tiefling_Levistus(Tiefling):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Legacy of Stygia", 1, "Spell"], Given={"1": "Ray of Frost", "3": "Armor of Agathys", "5": "Darkness"})

class Tiefling_Mammon(Tiefling):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Legacy of Minauros", 1, "Spell"], Given={"1": "Mage Hand", "3": "Tenser's Floating Disk", "5": "Arcane Lock"})

class Tiefling_Mephistopheles(Tiefling):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Legacy of Cania", 1, "Spell"], Given={"1": "Mage Hand", "3": "Burning Hands", "5": "Flame Blade"})

class Tiefling_Zariel(Tiefling):
    def __init__(self): 
        super().__init__()
        self.add_feature(meta=["Legacy of Avernus", 1, "Spell"], Given={"1": "Thaumaturgy", "3": "Searing Smite", "5": "Branding Smite"})

Catalog = {
    "Dragonborn": {
        "Base": Dragonborn,
        "Black": Dragonborn_Black,
        "Blue": Dragonborn_Blue,
        "Brass": Dragonborn_Brass,
        "Bronze": Dragonborn_Bronze,
        "Copper": Dragonborn_Copper,
        "Gold": Dragonborn_Gold,
        "Green": Dragonborn_Green,
        "Red": Dragonborn_Red,
        "Silver": Dragonborn_Silver,
        "White": Dragonborn_White
    },
    "Dwarf": {
        "Base": Dwarf,
        "Hill": Dwarf_Hill,
        "Mountain": Dwarf_Mountain
    },
    "Elf": {
        "Base": Elf,
        "Drow": Elf_Drow,
        "High": Elf_High,
        "Shadar_Kai": Elf_Shadar_Kai,
        "Wood": Elf_Wood
    },
    "Empty": {
        "Base": Empty
    },
    "Gnome": {
        "Base": Gnome,
        "Forest": Gnome_Forest,
        "Rock": Gnome_Rock
    },
    "Half_Orc": {
        "Base": Half_Orc,
        "Standard": Half_Orc_Standard
    },
    "Halfling": {
        "Base": Halfling,
        "Lightfoot": Halfling_Lightfoot,
        "Stout": Halfling_Stout
    },
    "Harengon": {
        "Base": Harengon,
        "Standard": Harengon_Standard
    },
    "Human": {
        "Base": Human,
        "Standard": Human_Standard
    },
    "Tiefling": {
        "Base": Tiefling,
        "Asmodeus": Tiefling_Asmodeus,
        "Baalzebul": Tiefling_Baalzebul,
        "Dispater": Tiefling_Dispater,
        "Fierna": Tiefling_Fierna,
        "Glasya": Tiefling_Glasya,
        "Levistus": Tiefling_Levistus,
        "Mammon": Tiefling_Mammon,
        "Mephistopheles": Tiefling_Mephistopheles,
        "Zariel": Tiefling_Zariel
    }
}

def get_Race_Data(main, sub, Level, PB):
    if main not in Catalog: return None
    group = Catalog[main]
    
    if sub and sub in group: data_dict = group[sub]()
    else: data_dict = group["Base"]()
        
    data_dict.Features = [f for f in data_dict.Features if f["Level"] <= Level]
    data_dict.Features.sort(key=lambda x: x["Level"])
    
    for data in data_dict.Features:
        tag = data.get("Tag")
        resolver = Feature_Map.get(tag)
        if resolver: resolver(data, data_dict, Level, PB)

    return data_dict