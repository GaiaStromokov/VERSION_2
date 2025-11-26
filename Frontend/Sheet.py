from Globals.UI.f_Utility import *
Tag = q.Tag
Rules = q.Rules
class pat_Sheet:
    def __init__(self, dbm):
        self.dbm = dbm
    
    def All(self):
        self.Core()
        
    def Core(self):
        Level, PB, R, SR, C, SC, BG = self.dbm.Vis.upd_Sheet
        configure_item(Tag.core.val.level(), label=Level)
        configure_item(Tag.core.val.pb(), label = f"PB: +{PB}")
        configure_item(Tag.core.select.r(), items=Rules.l.Race, default_value=R)
        configure_item(Tag.core.select.sr(), items=Rules.d.Race[R], default_value=SR)
        configure_item(Tag.core.select.c(), items=Rules.l.Class, default_value=C)
        configure_item(Tag.core.select.sc(), items=Rules.d.Class[C] if q.dbm.Validate.Class else [], default_value=SC)
        configure_item(Tag.core.select.bg(), items=Rules.l.Background, default_value=BG)
    # def Attributes(self):
    #     data=q.db.Atr
    #     for atr in Rules.list_Atr:
    #         cdata=data[atr]
    #         configure_item(Tag.atr.sum(atr), label = cdata.Val)
    #         configure_item(Tag.atr.mod(atr), label = cdata.Mod)
    #         configure_item(Tag.atr.select(atr), default_value = cdata.Base)
    #         configure_item(Tag.atr.source(atr, "Base"), label = cdata.Base)
    #         configure_item(Tag.atr.source(atr, "Race"), label = cdata.Rasi)
    #         configure_item(Tag.atr.source(atr, "Feat"), label = cdata.Milestone)

    # def Skills(self):
    #     data = q.dbm.Visual_Skill
    #     calc = q.dbm.Mod_Skill
    #     for skill in Rules.list_Skill:
    #         cdata=data[skill]
    #         configure_item(Tag.skill.toggle(skill), default_value=cdata)
    #         configure_item(Tag.skill.mod(skill), label=Rules.skill_text(calc[skill]))
    #         # configure_item(f"skill_Player_{skill}", default_value=skill in cdata["Player"])
    #         # configure_item(f"skill_Race_{skill}", default_value=skill in cdata["Race"])
    #         # configure_item(f"skill_Class_{skill}", default_value=skill in cdata["Class"])
    #         # configure_item(f"skill_BG_{skill}", default_value=skill in cdata["Background"])
    #         # configure_item(f"skill_Feat_{skill}", default_value=skill in cdata["Feat"])

    # def Health(self):
    #     data = q.dbm.Health.g.Visual
    #     configure_item(Tag.health.val("HP"), label = data.HP)
    #     configure_item(Tag.health.val("Temp"), label = data.Temp)
    #     set_value(Tag.health.val("Max"), data.Max)
        
    # def Initiative(self):
    #     data = q.dbm.Initiative.g.Visual
    #     configure_item(Tag.init.val(), label = data.Val)
    #     configure_item(Tag.init.source("Dex"), label = data.Dex)
    #     configure_item(Tag.init.source("Race"), label = data.Race)
    #     configure_item(Tag.init.source("Class"), label = data.Class)
    #     configure_item(Tag.init.source("Feat"), label = data.Milestone)
        
    # def Vision(self):
    #     cdata = q.dbm.Collect_Vision
    #     configure_item(Tag.vision.val(), label=cdata.Dark)
    #     for i in Rules.list_Vision:
    #         configure_item(Tag.vision.source(i), label=cdata[i])

    # def Speed(self):
    #     cdata = q.dbm.Collect_Speed
    #     configure_item(Tag.speed.val(), label=cdata.Walk)
    #     for i in Rules.list_Speed:
    #         configure_item(Tag.speed.source(i), label=cdata[i])


    # def AC(self):
    #     data = q.dbm.Armor.g.Visual
    #     configure_item(Tag.ac.val(), label = data.Sum)
    #     configure_item(Tag.ac.source("base"), label = data.Base)
    #     configure_item(Tag.ac.source("dex"), label = data.Dex)
    #     configure_item(Tag.ac.source("shield"), label = data.Shield)

    # def Conditions(self):
    #     for i in Rules.list_Condition:
    #         configure_item(Tag.cond.toggle(i),default_value = q.db.Condition[i])
    #         configure_item(Tag.cond.text(i), color = Rules.condition_color(i))

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

    # def Prof(self):
    #     cdata = q.dbm.Collect_Prof
    #     for i in q.w.search(Tier=0, Slot="Weapon", Cat="Simple"):
    #         configure_item(Tag.prof.toggle("Simple", i), default_value=i in cdata.Weapon)
    #         configure_item(Tag.prof.text("Simple", i), color=Rules.prof_color("Weapon", i))

    #     for i in q.w.search(Tier=0, Slot="Weapon", Cat="Martial"):
    #         configure_item(Tag.prof.toggle("Martial", i), default_value=i in cdata.Weapon)
    #         configure_item(Tag.prof.text("Martial", i), color=Rules.prof_color("Weapon", i))

    #     for i in q.w.search(Tier=0, Slot=["Armor", "Shield"]):
    #         configure_item(Tag.prof.toggle("Armor", i), default_value=i in cdata.Armor)
    #         configure_item(Tag.prof.text("Armor", i), color=Rules.prof_color("Armor", i))

    #     for i in Rules.list_Job:
    #         configure_item(Tag.prof.toggle("Artisan", i), default_value=i in cdata.Tool)
    #         configure_item(Tag.prof.text("Artisan", i), color=Rules.prof_color("Tool", i))

    #     for i in Rules.list_Game:
    #         configure_item(Tag.prof.toggle("Gaming", i), default_value=i in cdata.Tool)
    #         configure_item(Tag.prof.text("Gaming", i), color=Rules.prof_color("Tool", i))

    #     for i in Rules.list_Music:
    #         configure_item(Tag.prof.toggle("Musical", i), default_value=i in cdata.Tool)
    #         configure_item(Tag.prof.text("Musical", i), color=Rules.prof_color("Tool", i))

    #     for i in Rules.list_Lang:
    #         configure_item(Tag.prof.toggle("Languages", i), default_value=i in cdata.Lang)
    #         configure_item(Tag.prof.text("Languages", i), color=Rules.prof_color("Lang", i))