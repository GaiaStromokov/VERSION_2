from Globals.UI.f_Utility import *
Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing

class pat_Class:
    def __init__(self, dbm):
        self.dbm = dbm
        self.parent = Tag.block.c.feature()
        self.fHandle = {"Select": self.gen_Select,"Use": self.gen_Use,"Use_Select": self.gen_Use_Select,"Passive": self.gen_Passive,"Familiar": self.gen_Familiar}
    
    @property
    def db(self):
        return self.dbm.db
    
    def Refresh(self):
        self.Skill_Select()
        self.Features()
        
    def Skill_Select(self):
        pass
        
    def Features(self):
        icl(self.parent)
        for name, data in self.db.Class.Features.items():
            handler = self.fHandle.get(data["Tag"])
            temp = tgen(name)
            if handler: handler(temp.name,temp.tag, data)

    def gen_Passive(self, name, t, data):
            l_Desc = data["Desc"]
            t_header = Tag.block.c.feature.header(t)
            tl_Desc = [Tag.block.c.feature.text(t, f"{i+1}") for i in range(len(l_Desc))]
            
            with group(parent=self.parent):
                add_text(name, color=Coler.Header.G, tag=t_header)
                for i, Desc in enumerate(l_Desc):
                    add_text(dres(Desc), color=Coler.Text, wrap=sz.Wrap, tag=tl_Desc[i])

    def gen_Select(self, name, t, data):
        selection = data["Select"][0]
        item_list = data["Options"]
        t_header = Tag.block.c.feature.header(t)
        t_label = Tag.block.c.feature.label(t)
        t_popup = Tag.block.c.feature.popup(t)
        t_select = Tag.block.c.feature.select(t)

        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
                add_text(selection, color=Coler.Header.HP, tag=t_label)
            if "Desc" in data and data["Desc"]: add_text(data["Desc"][0], color=Coler.Text, wrap=sz.Wrap)

            idel(t_popup)
            with popup(t_header, mousebutton=mvMouseButton_Left, tag=t_popup):
                add_combo(items=item_list, default_value=selection, width=120, no_arrow_button=True, user_data=["Class Feature Select", t, 0], callback=q.cbh, tag=t_select)


    def gen_Use(self, name, t, data):
        l_Desc = data["Desc"]
        t_header = Tag.block.c.feature.header(t)
        tl_Desc = [Tag.block.c.feature.text(t, f"{i+1}") for i in range(len(l_Desc))]
        
        use_data = data["Use"]

        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
                for idx, val in enumerate(use_data):
                    t_toggle = Tag.block.c.feature.toggle(t, idx)
                    add_checkbox(default_value=val, enabled=True, user_data=["Class Feature Use", t, idx], callback=q.cbh, tag=t_toggle)

            for i, Desc in enumerate(l_Desc):
                add_text(dres(Desc), color=Coler.Text, wrap=sz.Wrap, tag=tl_Desc[i])
    
    def gen_Use_Select(self, name, t, data):
        t_header = Tag.block.c.feature.header(t)
        t_sel_1 = Tag.block.c.feature.select(t, "opt_1")
        t_sel_2 = Tag.block.c.feature.select(t, "opt_2")
        t_text_1 = Tag.block.c.feature.text(t, "opt_1")
        t_text_2 = Tag.block.c.feature.text(t, "opt_2")
        t_tool_1 = Tag.block.c.feature.tooltip(t, "opt_1")
        t_tool_2 = Tag.block.c.feature.tooltip(t, "opt_2")
        t_toggle_1 = Tag.block.c.feature.toggle(t, 1)
        t_toggle_2 = Tag.block.c.feature.toggle(t, 2)
        sel_1, sel_2 = data["Select"][1], data["Select"][2]
        
        sl_1, sl_2 = [""] + q.fTome(Level=data["Options"][1][1], Caster=data["Options"][1][0]), [""] + q.fTome(Level=data["Options"][2][1], Caster=data["Options"][2][0])
        use_1, use_2 = data["Use"][1], data["Use"][2]
        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
            with group(horizontal=True):
                add_text("Sel 1: ", color=Coler.Header.C)
                add_combo(items=sl_1, default_value=sel_1, width=150, no_arrow_button=True, callback=q.cbh, user_data=["Class Feature Select", t, 1], tag=t_sel_1)
                add_checkbox(default_value=use_1, enabled=True, user_data=["Class Feature Use", t, 1], callback=q.cbh, tag=t_toggle_1)
            with group(horizontal=True):
                add_text("Sel 2: ", color=Coler.Header.C)
                add_combo(items=sl_2, default_value=sel_2, width=150, no_arrow_button=True, callback=q.cbh, user_data=["Class Feature Select", t, 2], tag=t_sel_2)
                add_checkbox(default_value=use_2, enabled=True, user_data=["Class Feature Use", t, 2], callback=q.cbh, tag=t_toggle_2)


            idel(t_tool_1)
            with tooltip(t_sel_1, tag=t_tool_1):
                spell_detail(sel_1)
            idel(t_tool_2)
            with tooltip(t_sel_2, tag=t_tool_2):
                spell_detail(sel_2)
                
                
    def gen_Familiar(self, name, t, data):
        t_header = Tag.block.c.feature.header(t)
        t_desc = Tag.block.c.feature.text(t)
        t_hp = Tag.block.c.feature.HP(t)
        t_use = Tag.block.c.feature.toggle(t, 0)
        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
                add_text("---", color=Coler.Header.G)
                add_checkbox(default_value=data["Use"][0], enabled=True, callback=q.cbh, user_data=["Class Feature Use", t, 0], tag=t_use)
                add_text("---", color=Coler.Header.G)
                add_button(label="-", user_data=["Familiar Update", t, -1], width=20, callback=q.cbh)
                add_button(label=f"{data['HP']['Current']} / {data['HP']['Max']}",  enabled=False, tag=t_hp)
                add_button(label="+", user_data=["Familiar Update", t, 1], width=20, callback=q.cbh)
                

            with group(horizontal=True):
                add_text(data["Desc"][0], color=Coler.Text, wrap=sz.Wrap, tag=t_desc)

