from Globals.UI.f_Utility import *
Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing

t_tb = Tag.block.tabbar.Spells()
twindow_main = Tag.block.Spells.window()


tcast_Abil = Tag.spell.text("Abil")
tcast_Atk  = Tag.spell.text("Atk")
tcast_DC   = Tag.spell.text("DC")
tcast_window_A = Tag.Spells.Cast.A()
tcast_window_B = Tag.Spells.Cast.B()

tlearn_k_cantrip = Tag.Spells.Learn.Known.Cantrip()
tlearn_a_cantrip = Tag.Spells.Learn.Available.Cantrip()
tlearn_k_spell = Tag.Spells.Learn.Known.Spell()
tlearn_a_spell = Tag.Spells.Learn.Available.Spell()
tlearn_window_A = Tag.Spells.Learn.A()
tlearn_window_B = Tag.Spells.Learn.B()

tprep_current = Tag.Spells.Prepare.current()
tprep_available = Tag.Spells.Prepare.available()



class pat_Caster:
    def __init__(self, dbm):
        self.dbm = dbm
        self.data = None
        self.Cast = Cast(self)
        self.Learn = Learn(self)
        self.Prepare = Prepare(self)
    
    @property
    def db(self):
        return self.dbm.db
    
    def Refresh(self):
        self.data = self.dbm.db.Caster
        if self.data.Tog:
            show_item(t_tb)
            self.Cast.Refresh()
            self.Learn.Refresh()
            self.Prepare.Refresh()
        else:
            hide_item(t_tb)
    def Cast_Spell(self):
        self.Cast.Refresh_B()



class Cast:
    def __init__(self, parent):
        self.parent = parent
        self.data = None
        self.l_sh = ["Cantrip", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8", "Level 9"]
        

    def Refresh(self):
        self.data = self.parent.data
        self.Refresh_A()
        self.Refresh_B()

    def Refresh_A(self):
        configure_item(tcast_Abil, default_value=self.data.Abil)
        configure_item(tcast_Atk, default_value=self.data.Atk)
        configure_item(tcast_DC, default_value=self.data.DC)

    def Refresh_B(self):
        data = self.data
        icl(tcast_window_B)
        with group(parent=tcast_window_B):
            for level in range(0, data.MSL + 1):
                spell_list = data.Book[0] if level == 0 else data.Prepared[level]
                if not spell_list: continue
                with group(horizontal=False):
                    with group(horizontal=True):
                        add_text(self.l_sh[level], color=Coler.Header.B)
                        if level > 0:
                            for idx, value in enumerate(data.Slot[level]):
                                t = Tag.Spells.Cast.Toggle(level, idx)
                                add_checkbox(default_value=value, enabled=False, tag=t)
                    
                    button_label = "Cast" if level > 0 else "Will"
                    for spell in spell_list:
                        t_btn = Tag.Spells.Cast.Button(level, spell)
                        t_text = Tag.Spells.Cast.Text(level, spell)
                        t_tt = Tag.Spells.Cast.Tooltip(level, spell)
                        with group(horizontal=True):
                            add_button(label=button_label, width=50, user_data=["Spell Cast", level, spell], callback=q.cbh, tag=t_btn)
                            add_text(spell, color=Coler.Header.G, tag=t_text)
                            idel(t_tt)
                            with tooltip(t_text, tag=t_tt):
                                spell_detail(spell)
                    add_separator()


class Learn:
    def __init__(self, parent):
        self.parent = parent
        
    def Refresh(self):
        self.Refresh_A()
        self.Refresh_B()

    def Refresh_A(self):
        data = self.parent.data
        book = data.Book
        cantrips_known = len(book[0])
        spells_known = sum(len(book[level]) for level in range(1, 10))
        
        configure_item(tlearn_k_cantrip, default_value=cantrips_known)
        configure_item(tlearn_a_cantrip, default_value=data.CA)
        configure_item(tlearn_k_spell, default_value=spells_known)
        configure_item(tlearn_a_spell, default_value=data.SA)

    def Refresh_B(self):
        data = self.parent.data
        book = data.Book
        cast_list = self.parent.data.List
        
        for level in range(0, data.MSL + 1):
            t_win = Tag.Spells.Learn.WLevel(level)
            available_spells = q.fTome(Level=level, Caster=cast_list)
            current_spells = data.Book[level]
            icl(t_win)
            with group(parent=t_win):
                for spell in available_spells:
                    is_known = spell in current_spells
                    t_sel = Tag.Spells.Learn.Toggle(level, spell)
                    t_tt = Tag.Spells.Learn.Tooltip(level, spell)
                    
                    trigger = "Spell"
                    if level == 0: trigger = "Cantrip"
                    add_selectable(label=spell, default_value=is_known, width=680, user_data=["Spell Learn", spell, level, trigger], callback=q.cbh, tag=t_sel)
                    idel(t_tt)
                    with tooltip(t_sel, tag=t_tt):
                        spell_detail(spell)


class Prepare:
    def __init__(self, parent):
        self.parent = parent
        
    def Refresh(self):
        self.Refresh_A()
        self.Refresh_B()


    def Refresh_A(self):
        data = self.parent.data

        v_PA = data.PA
        if data.PA == 99999:
            v_PA = "INF"
            
            
            
        
        prepared = data.Prepared
        spells_preped = sum(len(prepared[level]) for level in range(1, 10))
        configure_item(tprep_current, default_value=spells_preped)
        configure_item(tprep_available, default_value=v_PA)

    def Refresh_B(self):
        data = self.parent.data
        for level in range(1, data.MSL + 1):
            t_win = Tag.Spells.Prepare.WLevel(level)
            known_spells = data.Book[level]
            prepared_spells = data.Prepared[level]
            icl(t_win)
            if not known_spells: continue
            with group(parent=t_win):
                for spell in known_spells:
                    t_sel = Tag.Spells.Prepare.Toggle(level, spell)
                    t_tt = Tag.Spells.Prepare.Tooltip(level, spell)
                    is_prepared = spell in prepared_spells
                    add_selectable(label=spell, default_value=is_prepared, width=680, user_data=["Spell Prepare", spell, level], callback=q.cbh, tag=t_sel)
                    idel(t_tt)
                    with tooltip(t_sel, tag=t_tt):
                        spell_detail(spell)