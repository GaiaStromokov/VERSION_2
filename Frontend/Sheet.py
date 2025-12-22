from Globals.UI.f_Utility import *
Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
class pat_Sheet:
    def __init__(self, dbm):
        self.dbm = dbm
    
    @property
    def db(self):
        return self.dbm.db

    def All(self):
        self.Core()
        self.Atr()
        
        self.Health()
        self.Initiative()
        
        self.Skill()
        self.Vision()
        self.Speed()
        self.Prof()
        
        self.Condition()

        
    def Core(self):
        Level, PB, R, SR, C, SC, BG = self.dbm.Vis.upd_Sheet
        configure_item(Tag.core.val.level(), label=Level)
        configure_item(Tag.core.val.pb(), label = f"PB: +{PB}")
        configure_item(Tag.core.select.r(), items=Rules.l.Race, default_value=R)
        configure_item(Tag.core.select.sr(), items=Rules.d.Race[R], default_value=SR)
        configure_item(Tag.core.select.c(), items=Rules.l.Class, default_value=C)
        configure_item(Tag.core.select.sc(), items=Rules.d.Class[C] if q.dbm.Validate.Class else [], default_value=SC)
        configure_item(Tag.core.select.bg(), items=Rules.l.Background, default_value=BG)

    def Atr(self):
        data = self.dbm.db.Atr
        for key, v in data.items():
            configure_item(Tag.atr.val(key), label=v.Val)
            configure_item(Tag.atr.mod(key), label=v.Mod)
            configure_item(Tag.atr.select(key), default_value=v.Base)
            configure_item(Tag.atr.source(key, "Base"), label=v.Base)
            configure_item(Tag.atr.source(key, "Race"), label=v.Race)
            configure_item(Tag.atr.source(key, "Feat"), label=v.Milestone)

    def Health(self):
        data = self.db.HP
        configure_item(Tag.health.hp(), label = f"{data.Current} / {data.Max}")
        configure_item(Tag.health.temp(), label = data.Temp)
        set_value(Tag.health.max(), data.Max)
        
    def Initiative(self):
        data = self.db.Initiative
        configure_item(Tag.init.val(), label = data.Val)
        configure_item(Tag.init.source("Dex"), label=self.db.Atr["DEX"].Mod)
        configure_item(Tag.init.source("Race"), label = data.Race)
        configure_item(Tag.init.source("Class"), label = data.Class)
        configure_item(Tag.init.source("Milestone"), label = data.Milestone)

    def Vision(self):
        data = self.db.Vision
        configure_item(Tag.vision.val(), label=data["Dark"].Val)
        for v in data:
            configure_item(Tag.vision.source(v), label=data[v].Val)

    def Speed(self):
        data = self.db.Speed
        configure_item(Tag.speed.val(), label=data["Walk"].Val)
        for v in data:
            configure_item(Tag.speed.source(v), label=data[v].Val)

    def Condition(self):
        data = self.db.Condition
        for key in data:
            i = data[key].Val
            configure_item(Tag.cond.toggle(key),default_value = i)
            configure_item(Tag.cond.text(key), color = Coler.Toggle(i))

    def Skill(self):
        data = self.db.Skill
        for key in data:
            d=data[key]
            configure_item(Tag.skill.toggle(key), default_value=d.Has)
            configure_item(Tag.skill.mod(key), label=d.tMod)
            # configure_item(f"skill_Player_{key}", default_value = key in cdata["Player"])
            configure_item(Tag.skill.source(key, "Race"), default_value = d.Race["prof"])
            configure_item(Tag.skill.source(key, "Class"), default_value = d.Class["prof"])
            configure_item(Tag.skill.source(key, "BG"), default_value = d.Background["prof"])
            configure_item(Tag.skill.source(key, "Milestone"), default_value = d.Milestone["prof"])


    def Prof(self):
        data = self.db.Prof
        
        d = data["Weapon"].Val
        
        for i in q.w.BSW:
            val = i in data["Weapon"].Val
            configure_item(Tag.prof.toggle("Simple", i), default_value=val)
            configure_item(Tag.prof.text("Simple", i), color=Coler.Toggle(val))

        for i in q.w.BMW:
            val = i in data["Weapon"].Val
            configure_item(Tag.prof.toggle("Martial", i), default_value=val)
            configure_item(Tag.prof.text("Martial", i), color=Coler.Toggle(val))

        for i in Rules.l.Armor:
            val = i in data["Armor"].Val
            configure_item(Tag.prof.toggle("Armor", i), default_value=val)
            configure_item(Tag.prof.text("Armor", i), color=Coler.Toggle(val))

        for i in Rules.l.Job:
            val = i in data["Tool"].Val
            configure_item(Tag.prof.toggle("Artisan", i), default_value=val)
            configure_item(Tag.prof.text("Artisan", i), color=Coler.Toggle(val))

        for i in Rules.l.Game:
            val = i in data["Tool"].Val
            configure_item(Tag.prof.toggle("Gaming", i), default_value=val)
            configure_item(Tag.prof.text("Gaming", i), color=Coler.Toggle(val))

        for i in Rules.l.Music:
            val = i in data["Tool"].Val
            configure_item(Tag.prof.toggle("Musical", i), default_value=val)
            configure_item(Tag.prof.text("Musical", i), color=Coler.Toggle(val))

        for i in Rules.l.Lang:
            val = i in data["Lang"].Val
            configure_item(Tag.prof.toggle("Languages", i), default_value=val)
            configure_item(Tag.prof.text("Languages", i), color=Coler.Toggle(val))


    # def AC(self):
    #     data = q.dbm.Armor.g.Visual
    #     configure_item(Tag.ac.val(), label = data.Sum)
    #     configure_item(Tag.ac.source("base"), label = data.Base)
    #     configure_item(Tag.ac.source("dex"), label = data.Dex)
    #     configure_item(Tag.ac.source("shield"), label = data.Shield)



    # def Char(self):
    #     cdata=q.db.Characteristic
    #     for i in Rules.list_Ideals:
    #         name = i.lower()
    #         configure_item(Tag.char.input(name), default_value=cdata[i])
    #         configure_item(Tag.char.text(name), default_value=cdata[i])
        
    #     cdata=q.db.Description
    #     for i in Rules.list_Description:
    #         configure_item(Tag.pDesc.input(i), default_value=cdata[i])
    #         configure_item(Tag.pDesc.text(i), default_value=cdata[i])

