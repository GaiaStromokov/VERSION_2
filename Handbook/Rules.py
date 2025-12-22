from box import Box



class collect_dicts:
    def __init__(self):
        self.Fighting_Style = Box({"Archery": "You gain a +2 bonus to attack rolls you make with ranged weapons.","Defense": "While you are wearing armor, you gain a +1 bonus to AC.","Dueling": "When you are wielding a melee weapon in one hand and no other weapons, you gain a +2 bonus to damage rolls with that weapon.","Great Weapon Fighting": "When you roll a 1 or 2 on a damage die for an attack you make with a melee weapon that you are wielding with two hands, you can reroll the die and must use the new roll. The weapon must have the two-handed or versatile property for you to gain this benefit.","Protection": "When a creature you can see attacks a target other than you that is within 5 feet of you, you can use your reaction to impose disadvantage on the attack roll. You must be wielding a shield.","Two Weapon Fighting": "When you engage in two-weapon fighting, you can add your ability modifier to the damage of the second attack.","Blind Fighting": "You have blindsight with a range of 10 feet. Within that range, you can effectively see anything that isn't behind total cover.","Interception": "When a creature you can see hits a target, other than you, within 5 feet of you with an attack, you can use your reaction to reduce the damage the target takes by 1d10 + PB. You must be wielding a shield or a simple or martial weapon to use this reaction.","Thrown Weapon Fighting": "You can draw a weapon that has the thrown property as part of the attack you make with the weapon. In addition, when you hit with a ranged attack using a thrown weapon, you gain a +2 bonus to the damage roll.","Unarmed Fighting": "Your unarmed strikes can deal bludgeoning damage equal to 1d6 + STR. If you aren't wielding any weapons or a shield when you make the attack roll, the d6 becomes a d8. At the start of each of your turns, you can deal 1d4 bludgeoning damage to one creature grappled by you."})
    
        self.Skill = Box({
            "Acrobatics": {"Atr": "DEX", "Desc": "Balance, flips, and avoiding being knocked down."},
            "Animal Handling": {"Atr": "WIS", "Desc": "Control and calm animals or read their behavior."},
            "Arcana": {"Atr": "INT", "Desc": "Knowledge of magic, spells, and magical traditions."},
            "Athletics": {"Atr": "STR", "Desc": "Climbing, jumping, swimming, and grappling."},
            "Deception": {"Atr": "CHA", "Desc": "Lying, bluffing, and misleading others."},
            "History": {"Atr": "INT", "Desc": "Recall historical facts, people, and events."},
            "Insight": {"Atr": "WIS", "Desc": "Detecting lies, motives, and emotions."},
            "Intimidation": {"Atr": "CHA", "Desc": "Threatening or coercing others into compliance."},
            "Investigation": {"Atr": "INT", "Desc": "Finding hidden clues or analyzing scenes."},
            "Medicine": {"Atr": "WIS", "Desc": "Stabilize the dying and diagnose illnesses."},
            "Nature": {"Atr": "INT", "Desc": "Knowledge of plants, animals, and the environment."},
            "Perception": {"Atr": "WIS", "Desc": "Noticing hidden things or sudden changes."},
            "Performance": {"Atr": "CHA", "Desc": "Acting, singing, dancing, and entertaining."},
            "Persuasion": {"Atr": "CHA", "Desc": "Convincing others with logic or charm."},
            "Religion": {"Atr": "INT", "Desc": "Understanding deities, rites, and dogma."},
            "Sleight of Hand": {"Atr": "DEX", "Desc": "Pickpocketing or manipulating objects subtly."},
            "Stealth": {"Atr": "DEX", "Desc": "Sneaking, hiding, and moving silently."},
            "Survival": {"Atr": "WIS", "Desc": "Tracking, finding food, and navigating the wild."}
        })

        self.Tool = Box({
            "Alchemist": "Job", "Brewer": "Job", "Calligrapher": "Job", "Carpenter": "Job", "Cartographer": "Job", "Cobbler": "Job", "Cook": "Job", "Glassblower": "Job", "Jeweler": "Job", "Leatherworker": "Job", "Mason": "Job", "Painter": "Job", "Potter": "Job", "Smith": "Job", "Tinker": "Job", "Weaver": "Job", "Thief": "Job", "Woodworker": "Job", "Navigator": "Job", "Disguise": "Job", "Forgery": "Job",
            "Dice": "Game", "Dragonchess": "Game", "Cards": "Game", "Three-Dragon Ante": "Game",
            "Bagpipes": "Music", "Drum": "Music", "Dulcimer": "Music", "Flute": "Music", "Lute": "Music", "Lyre": "Music", "Horn": "Music", "Pan Flute": "Music", "Shawm": "Music", "Viol": "Music"
        })
        self.Lang = Box({"Common": {},"Dwarvish": {},"Elvish": {},"Giant": {},"Gnomish": {},"Goblin": {},"Halfling": {},"Orc": {},"Abyssal": {},"Celestial": {},"Draconic": {},"Deep Speech": {},"Infernal": {},"Primordial": {},"Sylvan": {},"Undercommon": {}})

        self.Race = Box({
            "": [""],
            "Empty": [""],
            "Human": ["Standard", "Variant"],
            "Elf": ["High", "Drow", "Wood", "Shadar_Kai"],
            "Dwarf": ["Hill", "Mountain"],
            "Halfling": ["Lightfoot", "Stout"],
            "Gnome": ["Forest", "Rock"],
            "Dragonborn": ["Black", "Blue", "Brass", "Bronze", "Copper", "Gold","Green","Red","Silver","White"],
            "Half_Orc": ["Standard"],
            "Tiefling": ["Asmodeus","Baalzebul", "Dispater", "Fierna", "Glasya", "Levistus", "Mammon", "Mephistopheles", "Zariel"],
            "Harengon": ["Standard"]
        })
        self.Class = Box({
            "": [""],
            "Empty": [""],
            "Fighter": ["Champion", "Battle Master", "Eldritch_Knight", "Samuri"],
            "Wizard": ["Abjuration", "Conjuration"] 
        })
        
        self.Icon_Loader = {"Figure": ["Figure"],"Armor": ["Armor"],"Arms": ["Arms"],"Body": ["Body"],"Face": ["Face"],"Hands": ["Hands"],"Head": ["Head"],"Hand1": ["Hand_1"],"Hand2": ["Hand_2"],"Ring": ["Ring_1", "Ring_2"],"Shoulders": ["Shoulders"],"Throat": ["Throat"],"Waist": ["Waist"],"Feet": ["Feet"]}

class collect_lists:
    def __init__(self, d):
        self.d = d

        self.Race = list(self.d.Race.keys())
        self.Class = list(self.d.Class.keys())
        self.Background = ["Empty", "Charlatan","Criminal","Entertainer","Folk_Hero","Guild_Artisan","Hermit","Noble","Outlander","Sage","Sailor","Soldier","Urchin"]
        self.Atr = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        self.Prof = ["Weapon", "Armor", "Tool", "Lang"]
        self.Description = ["Gender", "Almnt", "Faith", "Size", "Age", "Hair", "Skin", "Eyes", "Height", "Weight"]
        self.Coins = ["CP", "SP", "GP", "PP"]
        self.Condition =  ["Blinded", "Charmed", "Deafened", "Frightened", "Grappled", "Incapacitated", "Invisible", "Paralyzed", "Petrified", "Poisoned", "Prone", "Restrained", "Stunned", "Unconscious", "Exhaustion"]

        self.Skill = list(self.d.Skill.keys())
        
        self.Job = [k for k, v in self.d.Tool.items() if v == "Job"]
        self.Game = [k for k, v in self.d.Tool.items() if v == "Game"]
        self.Music = [k for k, v in self.d.Tool.items() if v == "Music"]
        self.Lang = list(self.d.Lang.keys())
        self.Armor = ["Light", "Medium", "Heavy", "Shield"]
        
        
        self.Brand = ["Traits", "Ideals", "Bonds", "Flaws"]
        self.Vision = ["Dark", "Blind","Tremor","Tru"]
        self.Speed = ["Walk","Climb","Swim","Fly", "Burrow"]
        self.Equip_Type = ["Weapon", "Armor","Wand", "Staff", "Rod", "Potion", "Scroll", "Ring", "Wonderous", "Other"]
        self.Weapon_Atr = ["Name", "Range", "Hit", "Damage", "Type", "Notes"]
        self.Fighting_Style = list(self.d.Fighting_Style.keys())

class Rules:
    def __init__(self):
        self.d = collect_dicts()
        self.l = collect_lists(self.d)
        
    def fRarity(self, tier): return ["Common", "Uncommon", "Rare", "Very_Rare", "Legendary"][tier]