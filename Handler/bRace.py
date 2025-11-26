import q
from Handler.Utils.funcs import *
from Handbook.data_files.Races import *

class Loader:
    def __init__(self, parent, db, Level, PB):
        self.parent = parent
        self.db = db
        self.Level = Level
        self.PB = PB
        self.Map = {
            "Spell": self.Spell,
            "Select": self.Select,
            "Breath_Weapon": self.Breath_Weapon,
            "Use": self.Use,
            "HP": self.HP,
            "Passive": self.Passive
        }
        
        for feature in self.parent.Data.Features:
            name = feature["Name"].replace(" ", "_")
            tag = feature["Tag"]
            
            if tag in self.Map:
                self.Map[tag](feature, name)

    def Hplace(self, name, tag):
        place = self.db.Race.Features.setdefault(name, {})
        place["Tag"] = tag
        return place

    def get_past(self, Name, kind):
        past = self.parent.Past.get(Name, {})
        if kind == "Use": return past.get("Use", [])
        if kind == "Select": return past.get("Select", [])
        if kind == "Spell": return past.get("Spells", {})
        return {}

    def Spell(self, feature, Name):
        Place = self.Hplace(Name, "Spell")
        past = self.get_past(Name, "Spell")
        Place["Spells"] = {spell: past.get(spell, state) for spell, state in feature["Spells"].items()}

    def Select(self, feature, Name):

        Place = self.Hplace(Name, "Select")
        past = self.get_past(Name, "Select")
        Place["Choices"] = feature["Choices"]
        Place["Options"] = feature["Options"]
        Place["Select"] = (past + [""] * feature["Choices"])[:feature["Choices"]]
        
        if "Desc" in feature: Place["Desc"] = feature["Desc"]
        if "Multi_Desc" in feature: Place["Multi_Desc"] = feature["Multi_Desc"]

    def Breath_Weapon(self, feature, Name):
        Damage = feature["Damage"]
        Use = feature["Use"]
        Mod = self.db.Atr[feature["Save"]].Mod
        SV = 8 + self.PB + Mod
        
        Desc = feature["Desc"][0].format(Damage=Damage, SV=SV)
        
        Place = self.Hplace(Name, "Use")
        past = self.get_past(Name, "Use")
        Place["Use"] = (past + Use)[:len(Use)]
        Place["Desc"] = [Desc]

    def Use(self, feature, Name):
        Place = self.Hplace(Name, "Use")
        past = self.get_past(Name, "Use")
        Place["Use"] = (past + feature["Use"])[:len(feature["Use"])]
        Place["Desc"] = feature["Desc"]

    def HP(self, feature, Name):
        Place = self.Hplace(Name, "Passive")
        Place["Desc"] = feature["Desc"]

    def Passive(self, feature, Name):
        Place = self.Hplace(Name, "Passive")
        Place["Desc"] = feature["Desc"]

class bRace:
    def __init__(self, parent):
        self.parent = parent
        self.R = None
        self.SR = None
        self.L = None
        self.PB = None
        self.Data = None
        self.Past = None
    @property
    def db(self):
        return self.parent.db

    def Config_Vars(self):
        self.L, self.PB, self.R, self.SR = self.parent.Vis.Race

    def Startup(self):
        self.Config_Vars()
        self.Data = {}
        self.Past = self.db.Race.Features.copy()
        if not self.R: return
        self.Load_Data()

    def Load_Data(self):
        self.Data = get_Race_Data(self.R, self.SR, self.L, self.PB)
        if self.Data: 
            Loader(self, self.db, self.L, self.PB)
            self.Push_Data()

    def Push_Data(self):
        Data = self.Data
        Place = self.db
        
        p = Data.Speed
        for key, val in p.items():
            Place.Speed[key].Sit("Race", val)

        p = Data.Vision
        for key, val in p.items():
            Place.Vision[key].Sit("Race", val)

        p = Data.Combat.HP
        Place.HP.Sit("Race", p)
        
        p = Data.Combat.Initiative
        Place.Initiative.Sit("Race", p)
        
        p = Data.Prof
        for key in ["Weapon", "Armor", "Tool", "Lang"]:
            d = p[key]
            Place.Prof[key].Clear("Race")
            Place.Prof[key].Sit("Race", d)

        p = Data.Prof.Skill
        for skill in Place.Skill:
            if skill in p: Place.Skill[skill].Sit("Race", "prof", True)
            else: Place.Skill[skill].Sit("Race", "prof", False)

    def New(self):
        self.Config_Vars()
        self.Past = {}
        self.db.Race.fClear()
        if not self.R: return
        self.Load_Data()

    def Refresh(self):
        self.Config_Vars()
        self.Past = self.db.Race.Features.copy()
        if not self.R: return
        self.Load_Data()