import q
from Manager.Database import Database
from colorist import green, red
from box import Box
import inspect
import re
from Handler.bRace import bRace
from Frontend.Sheet import pat_Sheet
from Frontend.Race import pat_Race

def register_callback(key):
    def wrapper(func):
        func._callback_key = key
        return func
    return wrapper

class Populate:
    def __init__(self, parent):
        self.parent = parent
        self.Sheet = pat_Sheet(parent)
        self.R = pat_Race(parent)
        
    @property
    def db(self): return self.parent.db

    @property
    def Startup(self): 
        self.Basic
        self.Complicated
    
    @property
    def Basic(self): 
        self.Sheet.All()

    @property
    def Complicated(self): 
        self.R.Refresh()

    @property
    def Level(self): 
        self.Basic
        self.R.Refresh()
        
        
    @property
    def Race(self): 
        self.Basic
        self.R.Refresh()

class cb_Base:
    def __init__(self, parent, populate):
        self.parent = parent
        self.pat = populate
    
    @property
    def db(self):
        return self.parent.parent.db

class cb_Health(cb_Base):
    @register_callback("mod_HP")
    def mod_HP(self, sender, inp, udata):
        self.db.HP.Sit("Current", inp)

    @register_callback("mod_Temp")
    def mod_Temp(self, sender, inp, udata):
        self.db.HP.Sit("Temp", inp)

    @register_callback("mod_Base_HP")
    def mod_Base_HP(self, sender, inp, udata):
        self.db.HP.Sit("Player", inp)

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
    
    def Short(self):
        pass
    def Long(self):
        pass
        
class cb_Core(cb_Base):
    @register_callback("mod_Level")
    def Level(self, sender, inp, udata):
        data = udata[0]
        self.db.Core.Level.Sit(data)
        self.parent.dbm.Race.Refresh()
        self.pat.Level

    @register_callback("mod_Race")
    def mod_Race(self, sender, inp, udata):
        self.db.Core.Subrace.Sit("")
        self.db.Core.Race.Sit(inp)
        self.parent.dbm.Race.New()
        self.pat.Race

    @register_callback("mod_Subrace")
    def mod_Subrace(self, sender, inp, udata):
        self.db.Core.Subrace.Sit(inp)
        self.parent.dbm.Race.New()
        self.pat.Race

    @register_callback("mod_Background")
    def mod_Background(self, sender, inp, udata):
        self.db.Core.Background.Sit(inp)

    @register_callback("mod_Class")
    def mod_Class(self, sender, inp, udata):
        self.db.Core.Class.Sit(inp)

    @register_callback("mod_Subclass")
    def mod_Subclass(self, sender, inp, udata):
        self.db.Core.Subclass.Sit(inp)

class cb_Class(cb_Base):
    pass
        
class cb_Race(cb_Base):
    @register_callback("Race Feature Select")
    def Feature_Select(self, sender, inp, udata):
        key, index = udata
        self.db.Race.fSit_Select(key, index, inp)
        self.pat.Race

    @register_callback("Race Feature Use")
    def Feature_Use(self, sender, inp, udata):
        key, index = udata
        self.db.Race.fSit_Use(key, index, inp)

    @register_callback("Race Asi")
    def mod_Asi(self, sender, inp, udata):
        StatName = udata[0]
        self.db.Atr[StatName].Sit("Race", inp)
        

class cb_Atr(cb_Base):
    @register_callback("Base_Atr")
    def Base(self, sender, inp, udata):
        StatName = udata[0]
        self.db.Atr[StatName].Sit("Base", inp)


class CBH:
    def __init__(self, parent):
        self.parent = parent
        populate = self.parent.populate
        
        self.cb_closet = cb_Closet(self, populate)
        self.cb_rest = cb_Rest(self, populate)
        self.cb_health = cb_Health(self, populate)
        self.cb_core = cb_Core(self, populate)
        self.cb_race = cb_Race(self, populate)
        self.cb_class = cb_Class(self, populate)
        self.cb_atr = cb_Atr(self, populate)

        self.Input_map = {}
        for name, obj in inspect.getmembers(self):
            if name.startswith("cb_"):
                self.Input_map.update({
                    func._callback_key: func
                    for _, func in inspect.getmembers(obj, inspect.ismethod)
                    if hasattr(func, "_callback_key")
                })

    @property
    def dbm(self):
        return self.parent
    def sit(self, sender, data, udata):
        if not udata: return
        key, *params = udata
        func = self.Input_map.get(key)
        if not func:
            red(f"[CBH] Unknown key: {key}")
            return
        print(f"Sit: sender - {sender}, key - {key}, params - {params}")
        func(sender, data, params)

    def callback_func(self):
        return self.sit

class Validate:
    def __init__(self, parent):
        self.parent = parent
    
    @property
    def Class(self):
        Class, Level = self.parent.Vis.v_Class
        
        class_exception_map = {1: ["Cleric, Warlock"], 2: ["Wizard"]}
        return Level >= 3 or Class in class_exception_map.get(Level, [])
    
class Vis:
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
    
    @property
    def Race(self):
        data = self.db.Core
        return data.Level.Val, data.Level.PB, data.Race.Val, data.Subrace.Val;

    @property
    def v_Class(self):
        data = self.db.Core
        return data.Class.Val, data.Level.Val

    @property
    def upd_Sheet(self):
        data = self.db.Core
        return data.Level.Val, data.Level.PB, data.Race.Val, data.Subrace.Val, data.Class.Val, data.Subclass.Val, data.Background.Val;

    def Description(self, Desc):
            pb = self.db.Core.Level.PB
            
            Desc = re.sub(r'(\d*)PB', lambda m: str(int(m.group(1) or 1) * pb), Desc)
            Desc = re.sub(r'\b(STR|DEX|CON|INT|WIS|CHA)\b', lambda m: str(self.db.Atr[m.group(1)].Mod), Desc)
            
            return Desc
class DBM:
    def __init__(self):
        self.db = Database()
        self.populate = Populate(self)
        self.cbh = CBH(self)
        self.sit = self.cbh.sit
        self.Vis = Vis(self)
        self.Validate = Validate(self)
        
        self.Race = bRace(self)

    @property
    def Save_out(self):
        self.db.Save_out
    

    @property
    def Startup(self):
        self.Race.Startup()
        self.populate.Startup