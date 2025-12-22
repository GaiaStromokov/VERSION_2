import q, re, math
from Handler.Utils.funcs import *
from Handbook.data_files.Caster import *

class bCaster:
    def __init__(self, parent):
        self.parent = parent
        self.C = None
        self.SC = None
        self.L = None
        self.PB = None
        self.Data = None
        self.Past_Slot = None
        self.Past_Book = None
        self.Past_Prepared = None

    @property
    def db(self): return self.parent.db

    def Config_Vars(self):
        self.L, self.PB, self.C, self.SC = self.parent.Vis.ad_Class
    
    def Update(self):
        self.Config_Vars()
        if not self.C: return
        
        self.Past_Slot = [x[:] for x in self.db.Caster.Slot]
        self.Past_Book = [x[:] for x in self.db.Caster.Book]
        self.Past_Prepared = [x[:] for x in self.db.Caster.Prepared]

        self.Load_Data()
        self.Configure()
        self.Push_Data()

    def Startup(self):
        self.Update()

    def Refresh(self):
        self.Update()

    def New(self):
        self.Config_Vars()
        self.Data = {}
        if not self.C: return
        self.Load_Data()
        self.Push_Data()

    def Load_Data(self):
        self.Data = get_Caster_Data(self.C, self.SC, self.L)

    def Push_Data(self):
        Data = self.Data.Casting
        Place = self.db.Caster

        Place.MSL  = Data["MSL"]
        Place.CA   = Data["CA"]
        Place.SA   = Data["SA"]
        Place.Abil = Data["Abil"]
        Place.List = Data["List"]
        Place.Tog  = Data["Tog"]
        Place.PT   = Data["PT"]
        
        Place.Book = Data["Book"]
        Place.Prepared = Data["Prepared"]
        Place.Slot = Data["Slot"]
        Place.Sum()
    
    def Configure(self):
        data = self.Data.Casting
        
        msl = data["MSL"]
        slot = data["Slot"]
        p_slot = self.Past_Slot
        p_book = self.Past_Book
        p_prep = self.Past_Prepared

        for i in range(10):
            if i > msl:
                p_book[i] = []
                p_prep[i] = []
                slot[i] = []
            elif i < len(p_slot):
                slot[i] = (p_slot[i] + slot[i])[:len(slot[i])]
        
        data["Book"] = p_book
        data["Prepared"] = p_prep