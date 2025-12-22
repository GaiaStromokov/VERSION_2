import q, re, math
from Handler.Utils.funcs import *
from Handbook.data_files.Classes import *

class Loader:
    def __init__(self, parent, db, Level, PB):
        self.parent = parent; 
        self.db = db;
        self.Level = Level; 
        self.PB = PB
        
        self.Map = {"Select":self.Select,"Use":self.Use,"Use_Select":self.Use_Select,"Passive":self.Passive,"Familiar":self.Familiar}

        for feature in self.parent.Data.Features:
            name = feature["Name"].replace(" ", "_"); tag = feature["Tag"]
            if tag in self.Map: self.Map[tag](feature, name)


    def Hplace(self, name, tag):
        place = self.db.Class.Features.setdefault(name, {}); place["Tag"] = tag; return place

    def get_past(self, Name, kind):
        past = self.parent.Past.get(Name, {}); 
        if kind=="Use": return past.get("Use", [])
        if kind=="Select": return past.get("Select", [])
        return {}

    def Select(self, feature, Name):
        Place = self.Hplace(Name, "Select")
        past = self.get_past(Name, "Select")
        c = feature["Choices"]
        Place["Choices"] = c
        Place["Options"] = feature["Options"]
        Place["Select"] = (past + [""]*c)[:c]
        if "Desc" in feature: Place["Desc"] = [d for d in feature["Desc"]]
        if "Multi_Desc" in feature: Place["Multi_Desc"] = {k:self.resolve_desc(v) for k,v in feature["Multi_Desc"].items()}

    def Use(self, feature, Name):
        Place = self.Hplace(Name, "Use")
        Place["Use"] = feature["Use"][:len(feature["Use"])]
        if "Recharge" in feature: Place["Recharge"] = feature["Recharge"]
        if "Desc" in feature: Place["Desc"] = [d for d in feature["Desc"]]

    def Use_Select(self, feature, Name):
        Place = self.Hplace(Name, "Use_Select")
        past_use = self.get_past(Name, "Use")
        past_sel = self.get_past(Name, "Select")

        Options = [[]] + feature["Options"]
        count = len(Options)

        Place["Choices"] = feature["Choices"]
        Place["Options"] = Options
        Place["Select"] = (past_sel + [""]*count)[:count]
        Place["Use"] = [False] + (past_use + feature["Use"])[:len(feature["Use"])]

        if "Recharge" in feature: Place["Recharge"] = feature["Recharge"]
        if "Desc" in feature: Place["Desc"] = [d for d in feature["Desc"]]

    def Familiar(self, feature, Name):
        Place = self.Hplace(Name, "Familiar")
        _, stat = feature["HP"]
        Max = self.Level + self.db.Atr[stat].Mod
        Place["HP"] = {"Max":Max,"Current":Max}
        past_use = self.get_past(Name, "Use")
        Place["Use"] = (past_use + feature["Use"])[:len(feature["Use"])]
        if "Desc" in feature: Place["Desc"] = [d for d in feature["Desc"]]

    def Passive(self, feature, Name):
        Place = self.Hplace(Name, "Passive")
        if "Desc" in feature: Place["Desc"] = [d for d in feature["Desc"]]
        if "Amount" in feature: Place["Amount"] = feature["Amount"]

class bClass:
    def __init__(self, parent):
        self.parent = parent
        self.C = None
        self.SC = None
        self.L = None
        self.PB = None
        self.Data = None
        self.Past = None
    @property
    def db(self):
        return self.parent.db

    def Config_Vars(self):
        self.L, self.PB, self.C, self.SC = self.parent.Vis.ad_Class

    def Startup(self):
        self.Config_Vars()
        self.Data = {}
        self.Past = self.db.Class.Features.copy()
        if not self.C: return
        self.Load_Data()

    def Load_Data(self):
        self.Data = get_Class_Data(self.C, self.SC, self.L, self.PB)
        if self.Data: 
            Loader(self, self.db, self.L, self.PB)
            self.Push_Data()

    def Push_Data(self):
        Data = self.Data
        Place = self.db
        
        p = Data.Speed
        for key, val in p.items():
            Place.Speed[key].Sit("Class", val)

        p = Data.Vision
        for key, val in p.items():
            Place.Vision[key].Sit("Class", val)

        p = Data.Combat["HP"]
        Place.HP.Sit("Class", p)
        
        p = Data.Combat["Initiative"]
        Place.Initiative.Sit("Class", p)
        
        p = Data.Prof
        for key in ["Weapon", "Armor", "Tool", "Lang"]:
            d = p[key]
            Place.Prof[key].Clear("Class")
            Place.Prof[key].Sit("Class", d)

        p = Data.Prof["Skill"]
        for skill in Place.Skill:
            if skill in p: Place.Skill[skill].Sit("Class", "prof", True)
            else: Place.Skill[skill].Sit("Class", "prof", False)

    def New(self):
        self.Config_Vars()
        self.Data = {}
        self.Past = {}
        self.db.Class.Clear()
        if not self.C: return
        self.Load_Data()

    def Refresh(self):
        self.Config_Vars()
        self.Past = self.db.Class.Features.copy()
        self.db.Class.Clear()
        if not self.C: return
        self.Load_Data()