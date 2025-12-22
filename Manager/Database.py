from Functions.Pathing import get_path
from Handbook.Rules import Rules
import json

rules = Rules()

class tCaster:
    __slots__ = ('parent', 'Abil', 'Slot', 'Book', 'Prepared','List', 'Tog', 'PA', 'MSL', 'CA', 'SA', 'DC', 'Mod', 'Atk', 'PT')
    def __init__(self, parent, data):
        self.parent = parent
        self.Abil = "None"
        self.Slot = data["Slot"]
        self.Book = data["Book"]
        self.Prepared = data["Prepared"]
        self.List = ""
        self.Tog = False
        self.PA = 0
        self.MSL = 0
        self.CA = 0
        self.SA = 0
        self.DC = 0
        self.Mod = 0
        self.Atk = "+0"
        self.PT = ""
        self.Sum()

    def return_current(self, mode):
        if mode == "SK":  return sum(len(self.Book[i]) for i in range(1, 10))
        if mode == "SP":  return sum(len(self.Prepared[i]) for i in range(1, 10))
        if mode == "CK": return len(self.Book[0])
        return 0

    @property
    def save_data(self):
        return {"Slot": self.Slot, "Book": self.Book, "Prepared": self.Prepared}

    def Sum(self):
        if not self.Tog: return

        core = self.parent.Core
        atr  = self.parent.Atr
        
        L = core["Level"].Val
        PB = core["Level"].PB

        mod = atr[self.Abil].Mod
        self.Mod = mod
        self.DC  = 8 + PB + mod
        self.Atk = f"{PB + mod:+}"
        
        if self.PT == "Full": self.PA = max(1, L + mod)
        elif self.PT == "None": self.PA = 99999
        else: self.PA = 0

    def Max_Check(self, Spell, Level, Lookup, Current, Max):
        target = self.Book[Level] if Lookup == "B" else self.Prepared[Level]
        
        if Spell in target:
            target.remove(Spell)
            return

        c = self.return_current(Current)
        m = {"SA": self.SA, "CA": self.CA, "PA": self.PA}[Max]
        
        if c < m: target.append(Spell)

class tLevel:
    __slots__ = ('parent', 'Val', 'PB')
    l_prof = [0,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6]

    def __init__(self, parent, val):
        self.parent = parent
        self.Val = val
        self.PB = self.l_prof[val]

    def Sit(self, val):
        self.Val = max(1, min(int(self.Val + val), 20))
        self.PB = self.l_prof[self.Val]
        p = self.parent
        p.HP.Sum()
        # p.Caster.Sum()
        p.Update_Profs()
        p.Update_Skills()

class tCore:
    __slots__ = ('parent', 'Name', 'Val')
    def __init__(self, parent, name, val):
        self.parent = parent
        self.Name = name
        self.Val = val

    def Sit(self, val):
        self.Val = str(val).replace(" ", "_")

class tInitiative:
    __slots__ = ('parent', 'Race', 'Class', 'Milestone', 'Val')
    def __init__(self, parent, data):
        self.parent = parent
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]
        self.Val = 0
        self.Sum()

    @property
    def save_data(self):
        return {k: getattr(self, k) for k in ["Race", "Class", "Milestone"]}

    def Sum(self):
        atr = self.parent.Atr
        self.Val = atr["DEX"].Mod + self.Race + self.Class + self.Milestone

    def Sit(self, cat, val):
        setattr(self, cat, int(val))
        self.Sum()

class tHP:
    __slots__ = ('parent', 'Temp', 'Player', 'Race', 'Class', 'Milestone', 'Current', 'Max')
    def __init__(self, parent, data):
        self.parent = parent
        self.Temp = data["Temp"]
        self.Player = data["Player"]
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]
        self.Current = data["Current"]
        self.Max = 0
        self.Sum()

    @property
    def save_data(self):
        return {
            "Temp": self.Temp,
            "Player": self.Player,
            "Race": self.Race,
            "Class": self.Class,
            "Milestone": self.Milestone,
            "Current": self.Current
        }

    def Sum(self):
        lvl = self.parent.Core["Level"].Val
        con = self.parent.Atr["CON"].Mod
        self.Max = self.Player + self.Race + self.Class + self.Milestone + lvl * con

    def Heal(self, amt):
        self.Current = min(self.Current + amt, self.Max)

    def Damage(self, amt):
        use = min(self.Temp, amt)
        self.Temp -= use
        self.Current = max(self.Current - (amt - use), 0)


    def Mod_Temp(self, val):
        self.Temp = max(self.Temp + val, 0)

    def Sit(self, cat, val):
        v = int(val)
        if cat == "Temp": self.Mod_Temp(v)
        elif cat == "Current":
            if v >= 0: self.Heal(v)
            else: self.Damage(-v)
        else:
            setattr(self, cat, v)
        
        self.Sum()

class tRace:
    __slots__ = ('parent', 'Features')
    def __init__(self, parent, data):
        self.parent = parent
        self.Features = data["Features"]

    @property
    def save_data(self):
        return {"Features": self.Features}

    def Sit_Select(self, key, idx, inp):
        self.Features[key]["Select"][idx] = inp

    def Sit_Use(self, key, idx, inp):
        self.Features[key]["Use"][idx] = inp

    def Clear(self):
        self.Features = {}

class tClass:
    __slots__ = ('parent', 'Features', 'Skill')
    def __init__(self, parent, data):
        self.parent = parent
        self.Features = data["Features"]
        self.Skill = data["Skill"]

    @property
    def save_data(self):
        return {"Skill": self.Skill, "Features": self.Features}

    def Sit_Use_Select(self, key, n, idx, inp):
        self.Features[key][f"Select{n}"][idx] = inp
        
    def Sit_Select(self, key, idx, inp):
        self.Features[key]["Select"][idx] = inp

    def Sit_Use(self, key, idx, inp):
        self.Features[key]["Use"][idx] = inp

    def Familiar_Update(self, key, num):
        ward_data = self.Features[key]["HP"]
        new_hp = ward_data["Current"] + num
        ward_data["Current"] = max(0, min(new_hp, ward_data["Max"]))


    def Clear(self):
        self.Features = {}

class tSkill:
    __slots__ = ('parent', 'Atr', 'Desc', 'Race', 'Class', 'Milestone', 'Background', 'Has', 'Mod', 'tMod')
    def __init__(self, parent, name, data):
        self.parent = parent
        r = rules.d.Skill[name]
        self.Atr = r["Atr"]
        self.Desc = r["Desc"]
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]
        self.Background = data["Background"]
        self.Has = False
        self.Mod = 0
        self.tMod = ""
        self.Sum()

    @property
    def save_data(self):
        return {"Race": self.Race, "Class": self.Class, "Milestone": self.Milestone, "Background": self.Background}

    def Sum(self):
        atr = self.parent.Atr
        pb = self.parent.Core["Level"].PB
        sources = (self.Race, self.Class, self.Milestone, self.Background)
        has = any(src["prof"] for src in sources)
        exp = any(src["exp"] for src in sources)
        mod = atr[self.Atr].Mod
        if has: mod += pb
        if exp: mod += pb
        self.Mod = mod
        self.Has = has
        self.tMod = f"{mod:+}"

    def Sit(self, cat, key, val):
        getattr(self, cat)[key] = val
        self.Sum()

class tProf:
    __slots__ = ('parent', 'Name', 'Base', 'Race', 'Class', 'Milestone', 'Background', 'Val')
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

    @property
    def save_data(self):
        return {"Base": self.Base, "Race": self.Race, "Class": self.Class, "Milestone": self.Milestone, "Background": self.Background}

    def Sit(self, cat, val):
        getattr(self, cat).extend(val)
        self.Sum()

    def Clear(self, cat):
        getattr(self, cat).clear()
        self.Sum()

    def Sum(self):
        combined = self.Base + self.Race + self.Class + self.Milestone + self.Background
        self.Val = list(dict.fromkeys(combined))

class tStat:
    __slots__ = ('parent', 'name', 'Base', 'Race', 'Milestone', 'Val', 'Mod')
    def __init__(self, parent, name, data):
        self.parent = parent
        self.name = name
        self.Base = data["Base"]
        self.Race = data["Race"]
        self.Milestone = data["Milestone"]
        self.Val = 0
        self.Mod = 0
        self.Sum()

    @property
    def save_data(self):
        return {"Base": self.Base, "Race": self.Race, "Milestone": self.Milestone}

    def Sum(self):
        self.Val = self.Base + self.Race + self.Milestone
        self.Mod = (self.Val - 10) // 2

    def Sit(self, cat, val):
        setattr(self, cat, int(val))
        self.Sum()
        if self.name == "DEX": self.parent.Initiative.Sum()
        if self.name == "CON": self.parent.HP.Sum()
        # self.parent.Caster.Update_Stat(self.name)
        self.parent.Update_Skills(self.name)

class tVS:
    __slots__ = ('parent', 'name', 'Race', 'Class', 'Feat', 'Val')
    def __init__(self, parent, name, data):
        self.parent = parent
        self.name = name
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Feat = data["Feat"]
        self.Val = 0
        self.Sum()

    @property
    def save_data(self):
        return {"Race": self.Race, "Class": self.Class, "Feat": self.Feat}

    def Sit(self, cat, val):
        setattr(self, cat, int(val))
        self.Sum()

    def Sum(self):
        self.Val = self.Race + self.Class + self.Feat

class tCondition:
    __slots__ = ('parent', 'Name', 'Val')
    def __init__(self, parent, name, data):
        self.parent = parent
        self.Name = name
        self.Val = data

    @property
    def save_data(self):
        return self.Val

    def Sit(self, toggle):
        self.Val = toggle


class Database:
    def __init__(self):
        with open(get_path("Dist", "db.json"), "r") as f:
            sheet = json.load(f)

        p = sheet["Core"]
        self.Core = {
            "Level": tLevel(self, p["Level"]),
            "Race": tCore(self, "Race", p["Race"]),
            "Subrace": tCore(self, "Subrace", p["Subrace"]),
            "Class": tCore(self, "Class", p["Class"]),
            "Subclass": tCore(self, "Subclass", p["Subclass"]),
            "Background": tCore(self, "Background", p["Background"]),
        }

        p = sheet["Atr"]
        self.Atr = {k: tStat(self, k, p[k]) for k in rules.l.Atr}

        p = sheet["Initiative"]
        self.Initiative = tInitiative(self, p)

        p = sheet["Vision"]
        self.Vision = {k: tVS(self, k, p[k]) for k in rules.l.Vision}

        p = sheet["Speed"]
        self.Speed = {k: tVS(self, k, p[k]) for k in rules.l.Speed}

        p = sheet["Prof"]
        self.Prof = {k: tProf(self, k, p[k]) for k in rules.l.Prof}

        p = sheet["Skill"]
        self.Skill = {k: tSkill(self, k, p[k]) for k in rules.l.Skill}

        p = sheet["Condition"]
        self.Condition = {k: tCondition(self, k, p[k]) for k in rules.l.Condition}
        
        self.HP = tHP(self, sheet["HP"])
        self.Race = tRace(self, sheet["Race"])
        self.Class = tClass(self, sheet["Class"])
        self.Caster = tCaster(self, sheet["Caster"])

    def Update_Skills(self, stat=None):
        if stat is None:
            for s in self.Skill.values():
                s.Sum()
        else:
            for s in self.Skill.values():
                if s.Atr == stat:
                    s.Sum()

    def Update_Profs(self):
        for p in self.Prof.values():
            p.Sum()

    @property
    def Save_out(self):
        sheet = {
            "Core": {k: v.Val for k, v in self.Core.items()},
            "Atr": {k: v.save_data for k, v in self.Atr.items()},
            "Vision": {k: v.save_data for k, v in self.Vision.items()},
            "Speed": {k: v.save_data for k, v in self.Speed.items()},
            "Initiative": self.Initiative.save_data,
            "HP": self.HP.save_data,
            "Prof": {k: v.save_data for k, v in self.Prof.items()},
            "Skill": {k: v.save_data for k, v in self.Skill.items()},
            "Race": self.Race.save_data,
            "Class": self.Class.save_data,
            "Condition": {k: v.save_data for k, v in self.Condition.items()},
            "Caster": self.Caster.save_data,
        }
        with open(get_path("Dist", "db.json"), "w") as f:
            json.dump(sheet, f, indent=4)