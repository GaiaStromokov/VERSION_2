import q
from Manager.Database import Database
from colorist import green, red
import inspect
import re
from Handler.Utils.Importer import bRace, bClass, bCaster
from Frontend.Utils.Importer import pat_Sheet, pat_Race, pat_Class, pat_Caster

def register_callback(key):
    def wrapper(func):
        func._callback_key = key
        return func
    return wrapper

class Populate:
    def __init__(self, parent):
        self.parent = parent
        self.S = pat_Sheet(parent)
        self.R = pat_Race(parent)
        self.C = pat_Class(parent)
        self.Cas = pat_Caster(parent)
        
        self._refresh_map = {
            "sheet": self.S.All,
            "race": self.R.Refresh,
            "class": self.C.Refresh,
            "caster": self.Cas.Refresh,
            "condition": self.S.Condition,
            "cast": self.Cas.Cast_Spell,
            "HP": self.S.Health
        }

    @property
    def db(self):
        return self.parent.db

    def update(self, *scopes):
        for scope in scopes:
            if method := self._refresh_map.get(scope):
                method()

    def fat(self):
        self.update("sheet", "race", "class", "caster")

    def Startup(self):
        self.fat()

    def Level(self):
        self.fat()

    def Race(self):
        self.update("sheet", "race")

    def Class(self):
        self.update("sheet", "class", "caster")
    
    def Caster(self):
        self.update("caster")
    
    def Condition(self):
        self.update("condition")

    def Caster_Cast(self):
        self.update("cast")

    def Sheet(self):
        self.update("sheet")

class cb_Base:
    def __init__(self, parent, populate):
        self.parent = parent
        self.pat = populate
    
    @property
    def db(self):
        return self.parent.parent.db

    def atr_check(self, stat):
            lookup = self.db.Caster
            if lookup.Tog and lookup.Abil == stat:
                self.parent.dbm.Caster.Refresh()
                self.pat.Caster()

class cb_Health(cb_Base):
    @register_callback("mod_HP")
    def mod_HP(self, sender, inp, udata):
        num = udata[0]
        self.db.HP.Sit("Current", num)
        self.pat.update("HP")

    @register_callback("mod_Temp")
    def mod_Temp(self, sender, inp, udata):
        num = udata[0]
        self.db.HP.Sit("Temp", num)
        self.pat.update("HP")

    @register_callback("mod_Base_HP")
    def mod_Base_HP(self, sender, inp, udata):
        self.db.HP.Sit("Player", inp)
        self.pat.update("HP")

class cb_Closet(cb_Base):
    @register_callback("Closet")
    def Closet_Dispatch(self, sender, inp, udata):
        pass
    
    def Clear(self):
        pass

    def Modify(self):
        pass

class cb_Rest(cb_Base):
    @register_callback("Rest")
    def Rest_Dispatch(self, sender, inp, udata):
        if inp == "Short": self.Short()
        elif inp == "Long": self.Long()
        self.pat.Sheet()

    def Short(self):
        pass

    def Long(self):
        pass

class cb_Condition(cb_Base):
    @register_callback("Condition")
    def Modify(self, sender, inp, udata):
        key = udata[0]
        self.parent.dbm.db.Condition[key].Sit(inp)
        self.pat.Condition()

class cb_Core(cb_Base):
    @register_callback("mod_Level")
    def Level(self, sender, inp, udata):
        data = udata[0]
        self.db.Core["Level"].Sit(data)
        if not self.parent.dbm.Validate.Class: self.db.Core["Subclass"].Sit("")
        self.parent.dbm.Race.Refresh()
        self.parent.dbm.Class.Refresh()
        self.parent.dbm.Caster.Refresh()
        self.pat.Level()

    @register_callback("mod_Race")
    def mod_Race(self, sender, inp, udata):
        self.db.Core["Subrace"].Sit("")
        self.db.Core["Race"].Sit(inp)
        self.parent.dbm.Race.New()
        self.pat.Race()

    @register_callback("mod_Subrace")
    def mod_Subrace(self, sender, inp, udata):
        self.db.Core["Subrace"].Sit(inp)
        self.parent.dbm.Race.New()
        self.pat.Race()

    @register_callback("mod_Class")
    def mod_Class(self, sender, inp, udata):
        self.db.Core["Subclass"].Sit("")
        self.db.Core["Class"].Sit(inp)
        self.parent.dbm.Class.New()
        self.parent.dbm.Caster.New()
        self.pat.Class()

    @register_callback("mod_Subclass")
    def mod_Subclass(self, sender, inp, udata):
        self.db.Core["Subclass"].Sit(inp)
        self.parent.dbm.Class.New()
        self.parent.dbm.Caster.New()
        self.pat.Class()

    @register_callback("mod_Background")
    def mod_Background(self, sender, inp, udata):
        self.db.Core["Background"].Sit(inp)
        self.pat.Sheet()

class cb_Class(cb_Base):
    @register_callback("Class Feature Select")
    def Feature_Select(self, sender, inp, udata):
        key, index = udata
        self.db.Class.Sit_Select(key, index, inp)
        self.pat.Class()

    @register_callback("Familiar Update")
    def Arcane_Ward(self, sender, inp, udata):
        key, num = udata
        self.db.Class.Familiar_Update(key, num)
        self.pat.Class()

class cb_Race(cb_Base):
    @register_callback("Race Feature Select")
    def Feature_Select(self, sender, inp, udata):
        key, index = udata
        self.db.Race.Sit_Select(key, index, inp)
        self.pat.Race()

    @register_callback("Race Feature Use")
    def Feature_Use(self, sender, inp, udata):
        key, index = udata
        self.db.Race.Sit_Use(key, index, inp)
        self.pat.Race()

    @register_callback("Race Asi")
    def mod_Asi(self, sender, inp, udata):
        stat = udata[0]
        self.db.Atr[stat].Sit("Race", inp)
        self.atr_check(stat)
        self.pat.Race()

class cb_Atr(cb_Base):
    @register_callback("Base_Atr")
    def Base(self, sender, inp, udata):
        stat = udata[0]
        self.db.Atr[stat].Sit("Base", inp)
        self.atr_check(stat)
        self.pat.Level()

class cb_Caster(cb_Base):    
    @register_callback("Spell Cast")
    def Cast(self, sender, inp, udata):
        level, spell = udata
        slots = self.parent.dbm.db.Caster.Slot[int(level)]
        for i in range(len(slots)):
            if not slots[i]:
                slots[i] = True
                break
        self.pat.Caster_Cast()

    @register_callback("Spell Learn")
    def Learn(self, sender, inp, udata):
        spell, level, trigger = udata
        c, m = ("CK", "CA") if trigger == "Cantrip" else ("SK", "SA")
        self.parent.dbm.db.Caster.Max_Check(spell, level, "B", c, m)
        self.pat.Caster()

    @register_callback("Spell Prepare")
    def Prepare(self, sender, inp, udata):
        spell, level = udata
        self.parent.dbm.db.Caster.Max_Check(spell, level, "P", "SP", "PA")
        self.pat.Caster()
    
class CBH:
    def __init__(self, parent):
        self.parent = parent
        populate = self.parent.populate
        
        self.cb_closet = cb_Closet(self, populate)
        self.cb_rest = cb_Rest(self, populate)
        self.cb_health = cb_Health(self, populate)
        self.cb_core = cb_Core(self, populate)
        self.cb_condition = cb_Condition(self, populate)
        self.cb_race = cb_Race(self, populate)
        self.cb_class = cb_Class(self, populate)
        self.cb_caster = cb_Caster(self, populate)
        self.cb_atr = cb_Atr(self, populate)

        self.Input_map = {}
        for name, obj in inspect.getmembers(self):
            if name.startswith("cb_"): self.Input_map.update({func._callback_key: func for _, func in inspect.getmembers(obj, inspect.ismethod) if hasattr(func, "_callback_key")})

    @property
    def dbm(self):
        return self.parent

    def sit(self, sender, data, udata):
        key, *params = udata
        func = self.Input_map.get(key)
        if not func:
            red(f"[CBH] Unknown key: {key}")
            return
        # print(f"Sit: sender - {sender}, data - {data}, params - {params}")
        func(sender, data, params)

    def callback_func(self):
        return self.sit

class Validate:
    def __init__(self, parent):
        self.parent = parent
    
    @property
    def Class(self):
        Class, Level = self.parent.Vis.v_Class
        class_exception_map = {1: ["Cleric", "Warlock"], 2: ["Wizard"]}
        return Level >= 3 or Class in class_exception_map.get(Level, [])

class Vis:
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
    
    @property
    def ad_Race(self):
        data = self.db.Core
        return data["Level"].Val, data["Level"].PB, data["Race"].Val, data["Subrace"].Val

    @property
    def ad_Class(self):
        data = self.db.Core
        return data["Level"].Val, data["Level"].PB, data["Class"].Val, data["Subclass"].Val

    @property
    def v_Class(self):
        data = self.db.Core
        return data["Class"].Val, data["Level"].Val

    @property
    def upd_Sheet(self):
        data = self.db.Core
        return (
            data["Level"].Val, 
            data["Level"].PB, 
            data["Race"].Val, 
            data["Subrace"].Val, 
            data["Class"].Val, 
            data["Subclass"].Val, 
            data["Background"].Val
        )

class DBM:
    def __init__(self):
        self.db = Database()
        self.populate = Populate(self)
        self.cbh = CBH(self)
        self.sit = self.cbh.sit
        self.Vis = Vis(self)
        self.Validate = Validate(self)
        self.Race = bRace(self)
        self.Class = bClass(self)
        self.Caster = bCaster(self)

    @property
    def Save_out(self):
        self.db.Save_out
    
    @property
    def Startup(self):
        self.Race.Startup()
        self.Class.Startup()
        self.Caster.Startup()
        self.populate.Startup()