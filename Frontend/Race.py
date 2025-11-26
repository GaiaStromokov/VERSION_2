from Globals.UI.f_Utility import *
Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing

class pat_Race:
    def __init__(self, dbm):
        self.dbm = dbm
        self.parent = Tag.block.r.feature()
        self.fHandle = {"Select": self.gen_Select,"Use": self.gen_Use,"Passive": self.gen_Passive,"Spell": self.gen_Spell}
    
    @property
    def db(self):
        return self.dbm.db
    def Refresh(self):
        self.Ability_Scores()
        self.Features()
        
    def Ability_Scores(self):
        pass
        # configure_item(Tag.rfeature.select("asi_0"), default_value = q.db.Race.Rasi[0])
        # configure_item(Tag.rfeature.select("asi_1"), default_value = q.db.Race.Rasi[1])
        
    def Features(self):
        icl(self.parent)
        for name, data in self.db.Race.Features.items():
            handler = self.fHandle.get(data["Tag"])
            temp = tgen(name)
            if handler: handler(temp.name,temp.tag, data)

    def gen_Passive(self, name, t, data):
            l_Desc = data["Desc"]
            t_header = Tag.rfeature.header(t)
            tl_Desc = [Tag.rfeature.text(t, f"{i+1}") for i in range(len(l_Desc))]
            
            with group(parent=self.parent):
                add_text(name, color=Coler.Header.C, tag=t_header)
                for i, Desc in enumerate(l_Desc):
                    Desc = q.dbm.Vis.Description(Desc)
                    add_text(Desc, color=Coler.Text, wrap=sz.Wrap, tag=tl_Desc[i])

    def gen_Select(self, name, t, data):

        selection = data["Select"][0]
        item_list = data["Options"]
        t_header = Tag.rfeature.header(t)
        t_label = Tag.rfeature.label(t)
        t_tooltip = Tag.rfeature.tooltip(t)
        t_popup = Tag.rfeature.popup(t)
        t_select = Tag.rfeature.select(t)

        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
                add_text(selection, color=Coler.Header.HP, tag=t_label)
            if "Desc" in data and data["Desc"]: add_text(data["Desc"][0], color=Coler.Text, wrap=sz.Wrap)

            if "Multi_Desc" in data:
                t_mDesc = Tag.rfeature.Desc(t, "mDesc")
                if selection in data["Multi_Desc"]: add_text(data["Multi_Desc"][selection], color=Coler.Header.HP, tag=t_mDesc)
                else : add_text("", color=Coler.Header.HP, tag=t_mDesc)
            idel(t_tooltip)
            with tooltip(t_label, tag=t_tooltip):
                if selection in q.Grimoir:
                    spell_detail(selection)


            idel(t_popup)
            with popup(t_header, mousebutton=mvMouseButton_Left, tag=t_popup):
                add_combo(items=item_list, default_value=selection, width=120, no_arrow_button=True, user_data=["Race Feature Select", t, 0], callback=q.cbh, tag=t_select)


    def gen_Spell(self, name, t, data):
        t_header = Tag.rfeature.header(t)
        with group(parent=self.parent):
            add_text(name, color=Coler.Header.C, tag=t_header)
            spell_items = data["Spells"]

            for spell, val in spell_items.items():
                sdata = tgen(spell)
                t_label = Tag.rfeature.label(t, spell)
                t_tooltip = Tag.rfeature.tooltip(t, spell)

                with group(horizontal=True):
                    add_text(sdata.name, color=Coler.Header.G, tag=t_label)
                    if val == "Cantrip": add_text("At will", color=Coler.Header.HP)
                    else:
                        t_toggle = Tag.rfeature.toggle(t, spell)
                        add_checkbox(default_value=val, enabled=True, user_data=["Race Spell Use", t, sdata.tag], callback=q.cbh, tag=t_toggle)
                
                idel(t_tooltip)
                with tooltip(t_label, tag=t_tooltip):
                    spell_detail(sdata.name)
                        
                        
                
    def gen_Use(self, name, t, data):
        l_Desc = data["Desc"]
        t_header = Tag.rfeature.header(t)
        tl_Desc = [Tag.rfeature.text(t, f"{i+1}") for i in range(len(l_Desc))]
        
        use_data = data["Use"]

        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
                for idx, val in enumerate(use_data):
                    t_toggle = Tag.rfeature.toggle(t, idx)
                    add_checkbox(default_value=val, enabled=True, user_data=["Race Feature Use", t, idx], callback=q.cbh, tag=t_toggle)
            
            for i, Desc in enumerate(l_Desc):
                add_text(Desc, color=Coler.Text, wrap=sz.Wrap, tag=tl_Desc[i])