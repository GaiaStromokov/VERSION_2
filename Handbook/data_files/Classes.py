from box import Box
import q 
Rules = q.Rules


def Resolve_Select(data, parent, Level, PB):
    pass

def Resolve_Use(data, parent, Level, PB):
    rule = data["Use"]
    if isinstance(rule, list): count = rule[Level]
    elif isinstance(rule, int): count = rule
    elif isinstance(rule, str): count = PB if rule == "PB" else 0
    else: count = 0
    data["Use"] = [False] * count


def Resolve_Use_Select(data, parent, Level, PB):
    data["Use"] = [False] * data["Use"][Level]

def Resolve_Passive(data, parent, Level, PB):
    if "Amount" in data: data["Amount"] = data["Amount"][Level]

def Resolve_Familiar(data, parent, Level, PB):
    rule = data["Use"]
    count = rule[Level]
    data["Use"] = [False] * count


Feature_Map = {
    "Select": Resolve_Select,
    "Use": Resolve_Use,
    "Use_Select": Resolve_Use_Select,
    "Passive": Resolve_Passive,
    "Familiar": Resolve_Familiar
}


class Class_Template:
    def __init__(self, Level):
        self.Level = Level

        self.Speed = {"Walk": 0, "Climb": 0, "Swim": 0, "Fly": 0, "Burrow": 0}
        self.Vision = {"Dark": 0, "Blind": 0, "Tremor": 0, "Tru": 0}
        self.Prof = {"Skill": [], "Weapon": [], "Armor": [], "Tool": [], "Lang": []}
        self.Skill = {"Choices": 0, "Options": []}
        self.Saving_Throw = {"STR": False, "DEX": False, "CON": False, "INT": False, "WIS": False, "CHA": False}
        self.Combat = {"Initiative": 0, "HP": 0, "HD": 0}

        self.Features = []
        

    def add_feature(self, meta, Desc=None, Optional_Feature=None, **kwargs):
        name, level, tag = meta
        data = {"Name": name, "Level": level, "Tag": tag}
        if Desc: data["Desc"] = Desc
        if Optional_Feature: data["Optional_Feature"] = Optional_Feature
        data.update(kwargs)
        self.Features.append(data)

    def remove_feature(self, name):
        self.Features = [f for f in self.Features if f["Name"] != name]

    def modify_feature(self, meta, **kwargs):
        name, lvl = meta
        if self.Level < lvl: return
        for f in self.Features:
            if f["Name"] == name:
                f.update(kwargs)
                return



class Empty(Class_Template):
    def __init__(self, Level):
        super().__init__(Level)


class Fighter(Class_Template):
    def __init__(self, Level):
        super().__init__(Level)

        self.Prof["Armor"] = ["Light", "Medium", "Heavy", "Shield"]
        self.Prof["Weapon"] = q.w.BAW
        self.Skill["Choices"] = 2
        self.Skill["Options"] = ["Acrobatics","Animal Handling","Athletics","History","Insight","Intimidation","Perception","Survival"]
        self.Combat["HD"] = 10
        self.Saving_Throw["STR"] = True
        self.Saving_Throw["CON"] = True
        
        self.add_feature(meta=["Fighting_Style",1,"Select"],Choices=1,Options=Rules.l.Fighting_Style)
        self.add_feature(meta=["Second_Wind",1,"Use"],Use=[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],Recharge=["Short","Long"],Desc=["(bonus) regain 1d10 + {LEVEL} HP"])
        self.add_feature(meta=["Action_Surge",2,"Use"],Use=[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2],Recharge=["Short","Long"],Desc=["(free) take 1 additional action."])
        self.add_feature(meta=["Extra_Attack",5,"Passive"],Amount=[0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3],Desc=["(attack) Make {LEVEL//5} attacks"])
        self.add_feature(meta=["Indomitable",9,"Use"],Use=[0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3],Recharge="Long",Desc=["On Failed Save, reroll and use the new roll."])


class Fighter_Champion(Fighter):
    def __init__(self, Level):
        super().__init__(Level)

        self.add_feature(meta=["Improved_Critical",3,"Passive"],Desc=["Weapon attacks crit on 19-20"])
        self.add_feature(meta=["Remarkable_Athlete",7,"Passive"],Desc=["Add {PB} to non-proficient STR/DEX/CON checks.","Running long jump increases by {STR} ft"])
        self.modify_feature(meta=["Fighting_Style",10],Choices=2)
        if Level >= 15: self.remove_feature("Improved_Critical")
        self.add_feature(meta=["Superior_Critical",15,"Passive"],Desc=["Weapon attacks crit on 18-20"])
        self.add_feature(meta=["Survivor",18,"Passive"],Desc=["At start of turn, if at half HP or more, regain {CON} HP"])

class Fighter_Eldritch_Knight(Fighter):
    def __init__(self, Level):
        super().__init__(Level)
        self.add_feature(meta=["Weapon_Bond",3,"Passive"],Desc=["Bond with up to two weapons (1 hour ritual).","Cannot be disarmed of bonded weapon unless incapacitated.","Summon bonded weapon to hand as a Bonus Action."])

        self.add_feature(meta=["War_Magic",7,"Passive"],Desc=["When you use your action to cast a Cantrip, you can make one weapon attack as a bonus action"])
        self.add_feature(meta=["Eldritch_Strike",10,"Passive"],Desc=["(Attack) On Hit, Enemy has disadvantage on the next saving throw against your spells until the end of your next turn."])
        self.add_feature(meta=["Arcane_Charge",15,"Passive"],Desc=["(Action Surge) You may teleport up to 30 feet to an unoccupied space you can see."])
        if Level >= 18: self.remove_feature("War_Magic")
        self.add_feature(meta=["Improved_War_Magic",18,"Passive"],Desc=["When you use your action to cast a spell, you can make one weapon attack as a bonus action."])

class Wizard(Class_Template):
    def __init__(self, Level):
        super().__init__(Level)

        self.Prof["Weapon"] = ["Dagger","Dart","Sling","Quarterstaff","Light Crossbow"]
        self.Skill["Choices"] = 2
        self.Skill["Options"] = ["Arcana","History","Insight","Investigation","Medicine","Religion"]
        self.Combat["HD"] = 6
        self.Saving_Throw["INT"] = True
        self.Saving_Throw["WIS"] = True
        
        self.add_feature(meta=["Spellcasting",1,"Passive"],Desc=["You gots them magic hands."])
        self.add_feature(meta=["Arcane_Recovery",1,"Use"],Use=[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],Desc=["Recover spell slots of level {LEVEL//2} (max 6)"],Recharge="Long")
        self.add_feature(meta=["Spell_Mastery",18,"Use_Select"],Choices=1,Options=[["Wizard",1],["Wizard",2]],Use=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2],Recharge="Long")
        self.add_feature(meta=["Signature_Spells",20,"Use_Select"],Choices=1,Options=[["Wizard",3],["Wizard",3]],Use=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],Recharge="Long")


class Wizard_Conjuration(Wizard):
    def __init__(self, Level):
        super().__init__(Level)

        self.add_feature(meta=["Conjuration_Savant",2,"Passive"],Desc=["Cost/time to copy Conjuration spells halved."])
        self.add_feature(meta=["Minor_Conjuration",2,"Passive"],Desc=["(action) Conjure a non-magical item (3ft, 10 lb). Lasts 1 hour or until damaged."])
        self.add_feature(meta=["Benign_Transportation",6,"Use"],Use=[0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],Recharge="Long",Desc=["(action) Teleport 30 ft or swap places with a willing creature. Refreshes on casting a 1st-level+ Conjuration spell."])
        self.add_feature(meta=["Focused_Conjuration",10,"Passive"],Desc=["Damage does not break concentration on conjuration spells."])
        self.add_feature(meta=["Durable_Summons",14,"Passive"],Desc=["Summoned creatures have double HP."])


class Wizard_Abjuration(Wizard):
    def __init__(self, Level):
        super().__init__(Level)

        self.add_feature(meta=["Abjuration_Savant",2,"Passive"],Desc=["Cost/time to copy Abjuration spells halved."])
        self.add_feature(meta=["Arcane_Ward",2,"Familiar"],HP=["LEVEL","INT"],Use=[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],Recharge="Long",Desc=["On casting a 1st-level+ Abj spell, create a ward lasting until Long Rest. On Abj cast it regains {LEVEL} HP."])
        self.add_feature(meta=["Projected_Ward",6,"Passive"],Desc=["(reaction) Use your Arcane Ward to absorb damage dealt to a creature within 30 ft."])
        self.add_feature(meta=["Improved_Abjuration",10,"Passive"],Desc=["On Abj spell checks, add {PB}."])
        self.add_feature(meta=["Spell_Resistance",14,"Passive"],Desc=["Advantage on spell saves, resistance to spell damage."])




Catalog = {
    "Empty": {
        "Base": Empty
    },
    "Fighter": {
        "Base": Fighter,
        "Champion": Fighter_Champion,
        "Eldritch_Knight": Fighter_Eldritch_Knight
    },
    "Wizard": {
        "Base": Wizard,
        "Abjuration": Wizard_Abjuration,
        "Conjuration": Wizard_Conjuration
    }
}


def get_Class_Data(main, sub, Level, PB):
    if main not in Catalog: return None
    group = Catalog[main]

    if sub and sub in group: data_dict = group[sub](Level)
    else: data_dict = group["Base"](Level)

    data_dict.Features.sort(key=lambda x: x["Level"])
    data_dict.Features = [f for f in data_dict.Features if f["Level"] <= Level]

    for data in data_dict.Features:
        tag = data.get("Tag")
        resolver = Feature_Map.get(tag)
        if resolver: resolver(data, data_dict, Level, PB)

    return data_dict
