import q
from Utils.Handler_Utils import *

def dTemplate():
    return Box({
        "Speed": {"Walk": 0, "Climb": 0, "Swim": 0, "Fly": 0, "Burrow": 0},
        "Vision": {"Dark": 0, "Blind": 0, "Tremor": 0, "Tru": 0},
        "Prof": {"Skill": [], "Weapon": [], "Armor": [], "Tool": [], "Lang": []},
        "Combat": {"Initiative": 0, "HP": 0, "HD": 0},
        "Features": [],
        "Caster": None
    })

def Correct_Merge(End):
    data = dTemplate()
    for i in End.Speed.keys(): data.Speed[i] = End.Speed[i]
    for i in End.Vision.keys(): data.Vision[i] = End.Vision[i]
    for i in End.Prof.keys(): data.Prof[i] = End.Prof[i]
    for i in End.Combat.keys(): data.Combat[i] = End.Combat[i]
    data.Features = End.Features
    if "Caster" in End: data.Caster = End.Caster
    return data

class Tagger:
    def __init__(self, parent):
        self.parent = parent
        self.Level = self.parent.L
        self.PB = self.parent.PB
        Map = {
            "Select": self.Select,
            "Use": self.Use,
            "Passive": self.Passive,
            "Spell": self.Spell,
            "HP": self.HP,
        }
        for feature in self.parent.Data.Features:
            tag = feature.Tag
            Map[tag](feature)

    def Select(self, feature):
        if feature["Options"][0] == "0_Wizard":
            feature["Options"] = q.fTome(Level=0, Caster="Wizard")
    
    def Use(self, feature):
        vUse = feature["Use"]
        if isinstance(vUse, list): feature["Use"] = [False] * vUse[self.Level]
        elif isinstance(vUse, int): feature["Use"] = [False] * vUse
        elif vUse == "PB": feature["Use"] = [False] * self.PB
    
        if "lDesc" in feature: feature["Desc"] = feature["lDesc"][str(max(int(lvl) for lvl in feature["lDesc"] if int(lvl) <= self.Level))]
    
    
    def Passive(self, feature):
        pass
    
    def Spell(self, feature):
        feature["Spells"] = {spell: "Cantrip" if q.Grimoir[spell]["Level"] == 0 else False for spell in feature["Given"].values()}
        feature.pop("Spell", None)
    
    def HP(self, feature):
        if feature["HP"] == "LEVEL": feature["HP"] = self.Level

    
class Loader:
    def __init__(self, parent):
        self.parent = parent
        self.Level = self.parent.L
        self.PB = self.parent.PB
        Map = {
            "Spell": self.Spell,
            "Select": self.Select,
            "Breath_Weapon": self.Breath_Weapon,
            "Use": self.Use,
            "HP": self.HP,
            "Passive": self.Passive
        }
        
        for feature in self.parent.Data.Features:
            name = feature.Name.replace(" ", "_")
            level = feature.Level
            tag = feature.Tag
            if self.Level >= level:
                func = Map.get(tag)
                if func:
                    func(feature, name)

    def Hplace(self, name, tag):
        place = q.dbm.git.fRace.setdefault(name, {})
        place["Tag"] = tag
        return place

    def get_past(self, Name, kind):
        past = self.parent.Past.get(Name, {})
        if kind == "Use": return past.get("Use", [])
        if kind == "Select": return past.get("Select", [])
        if kind == "Spell": return past.get("Spells", {})
        return {}

    def Spell(self, feature, Name):
        Place = self.Hplace(Name, feature.Tag)
        past = self.get_past(Name, "Spell")
        Place["Spells"] = {spell: past.get(spell, state) for spell, state in feature.Spells.items()}

    def Select(self, feature, Name):
        Place = self.Hplace(Name, feature.Tag)
        past = self.get_past(Name, "Select")
        Place["Choices"] = feature.Choices
        Place["Options"] = feature.Options
        Place["Select"] = (past + [""] * feature.Choices)[:feature.Choices]
        if "Desc" in feature: Place["Desc"] = feature.Desc
        if "Multi_Desc" in feature: Place["Multi_Desc"] = feature.Multi_Desc

    def Breath_Weapon(self, feature, Name):
        Color = feature.Color
        Shape = feature.Shape
        Type = feature.Type
        Save = feature.Save
        Damage = feature.Damage[self.Level]
        SV = 8 + self.PB + 2
        Desc = feature.Desc[0].format(**locals())
        Place = self.Hplace(Name, "Use")
        past = self.get_past(Name, "Use")
        Place["Use"] = (past + [False])[:1]
        Place["Desc"] = [Desc]

    def Use(self, feature, Name):
        Place = self.Hplace(Name, feature.Tag)
        past = self.get_past(Name, "Use")
        Place["Use"] = (past + feature.Use)[:len(feature.Use)]
        Place["Desc"] = feature.Desc

    def HP(self, feature, Name):
        Place = self.Hplace(Name, "Passive")
        self.parent.Data.Combat.HP = feature.HP
        Place["Desc"] = feature.Desc

    def Passive(self, feature, Name):
        Place = self.Hplace(Name, feature.Tag)
        Place["Desc"] = feature.Desc

        

class bRace:
    def __init__(self, parent):
        self.parent = parent

        self.R = None
        self.SR = None
        self.L = None
        self.PB = None
        self.Data = None
        self.Past = None

    def Config_Vars(self):
        self.L, self.PB, self.R, self.SR = self.parent.pass_data.Race


    def Load_Start(self):
        self.Config_Vars()
        self.Data = {}
        self.Past = q.dbm.git.fRace
        if not self.R: return
        self.Load_Data()

    def Load_Data(self):
        path = f"Handbook/_Race/{self.R}"
        Merged = Box(load_json(path, "Base"))
        if self.SR in ["", "Empty"]: Subrace = dTemplate()
        else: Subrace = Box(load_json(path, self.SR))
        Merged = Correct_Merge(Merged)
        Subrace = Correct_Merge(Subrace)
        for k in Merged.Speed: Merged.Speed[k] += Subrace["Speed"][k]
        for k in Merged.Vision: Merged.Vision[k] += Subrace["Vision"][k]
        for k in Merged.Prof: Merged.Prof[k] = list(set(Merged.Prof[k] + Subrace["Prof"][k]))
        Merged.Features += Subrace["Features"]
        self.Data = Box(Merged)
        
        Tagger(self)
        Loader(self)
    
    def New(self):
        self.Config_Vars()
        self.Past = {}
        q.dbm.db.Race.Features = {}
        if not self.R: return
        self.Load_Data()
    
    def Refresh(self):
        self.Config_Vars()
        self.Past = self.Data.Features
        if not self.R: return
        self.Load_Data()