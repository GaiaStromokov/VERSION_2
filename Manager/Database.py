from Functions.Pathing import get_path
from Handbook.Rules import Rules
from box import Box
import json

rules = Rules()


class tCaster:
    def __init__(self, parent, data):
        self.parent = parent
        self.Spell_Abil = data["Spell_Abil"]
        self.Prep_Type = data["Prep_Type"]
        self.Caster_Type = data["Caster_Type"]
        self.L_Slot = data["L_Slot"]
        self.L_Max_Spell_Level = data["L_Max_Spell_Level"]
        self.L_Cantrips_Available = data["L_Cantrips_Available"]
        self.L_Spells_Available = data["L_Spells_Available"]
        self.Slot = data["Slot"]
        
        self.nPrep = 0
        self.Max_Spell_Level = 0
        self.Cantrips_Available = 0
        self.Spells_Available = 0
        
        self.DC = 0
        self.Mod = 0
        self.Atk = "+0"
        
        self.Sum()
    
    def Validate(self):
        Class = self.parent.Core.Class.Val
        Subclass = self.parent.Core.Subclass.Val
        
        valid_classes = ["Wizard"]
        valid_subclasses = ["Eldritch_Knight"]
        
        return Class in valid_classes or Subclass in valid_subclasses

    def Sum(self):
        if not self.Validate():
            self.Empty()
            return

        Level = self.parent.Core.Level.Val
        PB = self.parent.Core.Level.PB
        
        self.Slot = self.L_Slot[Level]
        self.Max_Spell_Level = self.L_Max_Spell_Level[Level]
        self.Cantrips_Available = self.L_Cantrips_Available[Level]
        self.Spells_Available = self.L_Spells_Available[Level]
        
        Mod = self.parent.Core.Atr[self.Spell_Abil].Mod
        self.Mod = Mod
        self.DC = 8 + PB + Mod
        
        val = PB + Mod
        self.Atk = f"+{val}" if val >= 0 else f"{val}"
        
        self.nPrep = Mod
        if self.Prep_Type == "Level":  self.nPrep += Level
        elif self.Prep_Type == "Half": self.nPrep += max(1, Level // 2)

    def Empty(self):
        self.Spell_Abil = ""
        self.Prep_Type = ""
        self.nPrep = 0
        self.Caster_Type = ""
        self.L_Slot = [[],[],[],[],[],[],[],[],[],[]] 
        self.L_Max_Spell_Level = []
        self.L_Cantrips_Available = []
        self.L_Spells_Available = []
        self.Slot = []
        self.Max_Spell_Level = 0
        self.Cantrips_Available = 0
        self.Spells_Available = 0
        self.DC = 0
        self.Mod = 0
        self.Atk = "+0"

    def Update_Stat(self, stat):
        if self.Spell_Abil == stat:
            self.Sum()


    
class tLevel:
    def __init__(self, parent, val):
        self.parent = parent
        self.Val = val
        self.PB = [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11][self.Val]
    
    def Sit(self, val):
        level = self.Val
        addition = val
        self.Val = max(1, min(int(level + addition), 20))
        self.PB = [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11][self.Val]
        self.parent.HP.Sum()
        self.parent.Caster.Sum()
        self.parent.Update_Profs()
        self.parent.Update_Skills()


class tCore:
    def __init__(self, parent, name, val):
        self.parent = parent
        self.Name = name
        self.Val = val
    
    def Sit(self, val):
        self.Val = str(val).replace(" ", "_")


class tInitiative:
    def __init__(self, parent, data):
        self.parent = parent
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]
        self.Val = 0
        self.Sum()
    
    def Sum(self):
        dex_mod = self.parent.Atr["DEX"].Mod
        self.Val = dex_mod + self.Race + self.Class + self.Milestone
    
    def Sit(self, cat, val):
        setattr(self, cat, int(val))
        self.Sum()


class tHP:
    def __init__(self, parent, data):
        self.parent = parent
        self.Temp = data["Temp"]
        self.Player = data["Player"]
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]
        self.Val = 0
        self.Current = data["Current"]
        self.Sum()
    
    def Sum(self):
        level = self.parent.Core.Level.Val
        con_mod = self.parent.Atr["CON"].Mod
        self.Val = self.Temp + self.Player + self.Race + self.Class + self.Milestone + (level * con_mod)
    
    def Sit(self, cat, val):
        setattr(self, cat, int(val))
        self.Sum()


class tRace:
    def __init__(self, parent, data):
        self.parent = parent
        self.Features = data["Features"]
    
    def fSit_Select(self, key, index, inp):
        self.Features[key]["Select"][index] = inp

    def fSit_Use(self, key, index, inp):
        self.Features[key]["Use"][index] = inp
    
    def fClear(self):
        self.Features = {}


class tClass:
    def __init__(self, parent, data):
        self.parent = parent
        self.Features = data["Features"]
        self.Skill = data["Skill"]
        
    def fSit_Select(self, key, index, inp):
        self.Features[key]["Select"][index] = inp

    def fSit_Use(self, key, index, inp):
        self.Features[key]["Use"][index] = inp


class tSkill:
    def __init__(self, parent, name, data):
        self.parent = parent
        rules_data = rules.d.Skill[name]
        self.Atr = rules_data["Atr"]
        self.Desc = rules_data["Desc"]
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]
        self.Background = data["Background"]
        self.Has = False
        self.Mod = 0
        self.tMod = ""
        self.Sum()

    def Sum(self):
        pb = self.parent.Core.Level.PB
        self.Has = any([self.Race["prof"], self.Class["prof"], self.Milestone["prof"], self.Background["prof"]])
        expert = any([self.Race["exp"], self.Class["exp"], self.Milestone["exp"], self.Background["exp"]])
        mod = self.parent.Atr[self.Atr].Mod
        if self.Has: mod += pb
        if expert: mod += pb
        self.Mod = mod
        self.tMod = f"{'+' if mod >= 0 else ''}{mod}"
    
    def Sit(self, cat, key, val):
        getattr(self, cat)[key] = val
        self.Sum()


class tProf:
    def __init__(self, parent, name, data):
        self.parent = parent
        self.Name = name
        self.Base = data["Base"]
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]
        self.Background = data["Background"]
        self.Val = []
        self.Sum()

    def Sit(self, cat, val):
        getattr(self, cat).extend(val)
        self.Sum()
        
    def Sum(self):
        self.Val = list(set(self.Base + self.Race + self.Class + self.Milestone + self.Background))


class tStat:
    def __init__(self, parent, name, data):
        self.parent = parent
        self.name = name
        self.Base = data["Base"]
        self.Race = data["Race"]
        self.Milestone = data["Milestone"]
        self.Val = 0
        self.Mod = 0
        self.Sum()

    def Sum(self):
        self.Val = self.Base + self.Race + self.Milestone
        self.Mod = (self.Val - 10) // 2

    def Sit(self, cat, val):
        setattr(self, cat, int(val))
        self.Sum()
        if self.name == "DEX": self.parent.Initiative.Sum()
        if self.name == "CON": self.parent.HP.Sum()
        self.parent.Caster.Update_Stat(self.name)
        self.parent.Update_Skills(self.name)


class tVS:
    def __init__(self, parent, data):
        self.parent = parent
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Feat = data["Feat"]
        self.Val = 0
        self.Sum()

    def Sit(self, cat, val):
        setattr(self, cat, int(val))
        self.Sum()

    def Sum(self):
        self.Val = self.Race + self.Class + self.Feat


class Database:
    def __init__(self):
        with open(get_path("Dist", "db.json"), "r") as f:
            sheet = json.load(f)

        d = sheet["Core"]
        self.Core = Box({
            "Level": tLevel(self, d["Level"]),
            "Race": tCore(self, "Race", d["Race"]),
            "Subrace": tCore(self, "Subrace", d["Subrace"]),
            "Class": tCore(self, "Class", d["Class"]),
            "Subclass": tCore(self, "Subclass", d["Subclass"]),
            "Background": tCore(self, "Background", d["Background"])
        })
        
        d = sheet["Atr"]
        self.Atr = Box({key: tStat(self, key, d[key]) for key in rules.l.Atr})
        
        self.Initiative = tInitiative(self, sheet["Initiative"])
        
        d = sheet["Vision"]
        self.Vision = Box({key: tVS(self, key, d[key]) for key in rules.l.Vision})
        
        d = sheet["Speed"]
        self.Speed = Box({key: tVS(self, key, d[key]) for key in rules.l.Speed})
        
        d = sheet["Prof"]
        self.Prof = Box({key: tProf(self, key, d[key]) for key in rules.l.Prof})
        
        d = sheet["Skill"]
        self.Skill = Box({key: tSkill(self, key, d[key], key) for key in rules.l.Skill})
        
        self.HP = tHP(self, sheet["HP"])
        
        self.Race = tRace(self, sheet["Race"])
        self.Class = tRace(self, sheet["Class"])
        self.Caster = tCaster(self, sheet["Caster"])

    def Update_Skills(self, stat=None):
        for skill in self.Skill.values():
            if stat is None or skill.Atr == stat:
                skill.Sum()

    def Update_Profs(self):
        for prof in self.Prof.values():
            prof.Sum()

    @property
    def Save_out(self):
        sheet = {
            "Core": {k: v.Val for k, v in self.Core.items()},
            "Atr": {k: {"Base": v.Base, "Race": v.Race, "Milestone": v.Milestone} for k, v in self.Atr.items()},
            "Vision": {k: {"Race": v.Race, "Class": v.Class, "Feat": v.Feat} for k, v in self.Vision.items()},
            "Speed": {k: {"Race": v.Race, "Class": v.Class, "Feat": v.Feat} for k, v in self.Speed.items()},
            "Initiative": {k: getattr(self.Initiative, k) for k in ["Race", "Class", "Milestone"]},
            "HP": {k: getattr(self.HP, k) for k in ["Temp", "Player", "Race", "Class", "Milestone", "Current"]},
            "Prof": {k: {"Base": v.Base, "Race": v.Race, "Class": v.Class, "Milestone": v.Milestone, "Background": v.Background} for k, v in self.Prof.items()},
            "Skill": {k: {"Race": v.Race, "Class": v.Class, "Milestone": v.Milestone, "Background": v.Background} for k, v in self.Skill.items()},
            "Race": {"Features": self.Race.Features},
            "Class": {"Features": self.Class.Features},
            "Caster": {k: getattr(self.Caster, k) for k in ["Spell_Abil", "Prep_Type", "Caster_Type", "L_Slot", "L_Max_Spell_Level", "L_Cantrips_Available", "L_Spells_Available", "Slot"]}
        }
        with open(get_path("Dist", "db.json"), "w") as f:
            json.dump(sheet, f, indent=4)
