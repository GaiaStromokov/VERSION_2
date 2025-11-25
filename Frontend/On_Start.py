from dearpygui.dearpygui import *
import q
from Globals.UI.c_Size import Sizing

sz = Sizing()
tag = q.Tag
Coler = q.Coler
Rules = q.Rules
get_path = q.get_path


def h_Atr_Row(stat: str):
    label_w = sz.Atr_Row.Label.w
    value_w = sz.Atr_Row.Val.w
    with group(horizontal=True):
        add_button(label=stat, enabled=False, width=label_w)
        add_button(label="", enabled=False, width=value_w, tag=tag.atr.sum(stat))
        add_button(label="", enabled=False, width=value_w, tag=tag.atr.mod(stat))
    with popup(tag.atr.sum(stat), mousebutton=mvMouseButton_Left):
        with group(horizontal=True):
            add_button(label="Base", enabled=False, width=label_w)
            add_combo(items=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], default_value="", width=value_w, no_arrow_button=True, user_data=["Base_Atr", stat], callback=q.cbh, tag=tag.atr.select(stat))
    with tooltip(tag.atr.sum(stat)):
        for source in ["Base", "Race", "Feat"]:
            with group(horizontal=True):
                add_button(label=source, enabled=False, width=label_w)
                add_button(label="", enabled=False, width=25, tag=tag.atr.source(stat, source))

def h_Skill_Row(skill: str):
    label_w = sz.Skill_Row.Label.w
    mod_w = sz.Skill_Row.Mod.w
    source_w = sz.Skill_Row.Source.w
    
    with group(horizontal=True):
        add_button(label=skill, enabled=False, width=label_w, tag=tag.skill.label(skill))
        add_checkbox(default_value=False, enabled=False, user_data=[], callback=q.cbh, tag=tag.skill.toggle(skill))
        add_button(label="", enabled=False, width=mod_w, tag=tag.skill.mod(skill))
    with tooltip(tag.skill.toggle(skill)):
        for source in ["Player", "Race", "Class", "BG", "Feat"]:
            with group(horizontal=True):
                add_button(label=source, enabled=False, width=source_w)
                add_checkbox(default_value=False, enabled=False, user_data=[""], callback=q.cbh, tag=tag.skill.source(skill, source))

def h_Char():
    with popup(tag.brand.char.label(), mousebutton=mvMouseButton_Left):
        for item in Rules.l.Description:
            with group(horizontal=True):
                add_button(label=item, enabled=False, width=sz.Btn.L.w)
                add_input_text(default_value="", on_enter=True, width=70, user_data=["Description", item], callback=q.cbh, tag=tag.brand.char.input(item))
    with tooltip(tag.brand.char.label()):
        for item in Rules.l.Description:
            with group(horizontal=True):
                add_button(label=item, enabled=False, width=sz.Btn.L.w)
                add_text("", color=Coler.Header.G, wrap=400, tag=tag.brand.char.text(item))




def h_Prof(tLabel: str, proficiency_map: dict):
    with popup(tLabel, mousebutton=mvMouseButton_Left):
        with group(horizontal=True):
            for category, items in proficiency_map.items():
                with child_window(auto_resize_x=True, auto_resize_y=True, border=True):
                    add_text(category)
                    add_separator()
                    for item in items:
                        add_selectable(label=item.replace("_", " "), default_value=False, user_data=["Player Prof Input", category, item], callback=q.cbh, tag=tag.prof.toggle(category,item))
    with tooltip(tLabel):
        with group(horizontal=True):
            for category, items in proficiency_map.items():
                with child_window(auto_resize_x=True, auto_resize_y=True, border=True):
                    add_text(category)
                    add_separator()
                    for item in items:
                        add_text(item.replace("_", " "), color=(0, 0, 0), tag=tag.prof.text(category,item))

def h_Stat_Window(label, tag_prefix, sources):
    btn_w = sz.Btn.M.w
    with group(parent=tag_prefix.window()):
        add_button(label=label, enabled=False, width=btn_w, tag=tag_prefix.label())
        add_button(label="", enabled=False, width=btn_w, tag=tag_prefix.val())
    with tooltip(tag_prefix.label()):
        for source in sources:
            with group(horizontal=True):
                add_button(label=source, enabled=False, width=50)
                add_button(label="", enabled=False, width=40, tag=tag_prefix.source(source))

def h_Core_Row(label, tag_select, user_data_key, max_w):
    btn_w = 80
    combo_w = max_w - 88
    with group(horizontal=True):
        add_button(label=label, enabled=False, width=btn_w)
        add_combo(width=combo_w, no_arrow_button=True, user_data=[user_data_key], callback=q.cbh, tag=tag_select)

def Load_Icons():
    icon_map = Rules.d.Icon_Loader

    with texture_registry(show=False):
        for file_base, tag_names in icon_map.items():
            file_path = get_path(f"Image/{file_base}_Icon.png")
            w, h, _, data = load_image(file_path)
            for tag_name in tag_names:
                add_static_texture(width=w, height=h, default_value=data, tag=tag.closet.icon(tag_name))

def c_Skeleton(): 
    with window(no_title_bar=True, no_close=True, autosize=True, tag=tag.main.window()):
        with group(horizontal=True):
            with group(horizontal=False):
                with group(horizontal=True):
                    with group(horizontal=False):
                        add_child_window(tag=tag.core.window(), width=sz.Core.w, height=sz.Core.h, border=True, no_scrollbar=True)
                        add_child_window(tag=tag.health.window(), width=sz.Health.w, height=sz.Health.h, border=True)
                        add_child_window(tag=tag.prof.window(), width=sz.Prof.w, height=sz.Prof.h, border=True)
                        add_child_window(tag=tag.brand.window(), width=sz.Char.w, height=sz.Char.h, border=True)
                        add_child_window(tag=tag.buffer1.window(), width=sz.Buffer2.w, height=sz.Buffer2.h, border=True, no_scrollbar=True)
                    with group(horizontal=False):
                        add_child_window(tag=tag.atr.window(), width=sz.Atr.w, height=sz.Atr.h, border=True)
                        with group(horizontal=True):
                            add_child_window(tag=tag.init.window(), width=sz.Init.w, height=sz.Init.h, border=True)
                            add_child_window(tag=tag.ac.window(), width=sz.AC.w, height=sz.AC.h, border=True)
                        with group(horizontal=True):
                            add_child_window(tag=tag.vision.window(), width=sz.Vision.w, height=sz.Vision.h, border=True)
                            add_child_window(tag=tag.speed.window(), width=sz.Speed.w, height=sz.Speed.h, border=True)
                        add_child_window(tag=tag.cond.window(), width=sz.Cond.w, height=sz.Cond.h, border=True)
                        add_child_window(tag=tag.rest.window(), width=sz.Rest.w, height=sz.Rest.h, border=True)
                        add_child_window(tag=tag.buffer2.window(), width=sz.Buffer1.w, height=sz.Buffer1.h, border=True, no_scrollbar=True)
                    with group(horizontal=False):
                        add_child_window(tag=tag.skill.window(), width=sz.Skill.w, height=sz.Skill.h, border=True, no_scrollbar=True)
                with group(horizontal=False):
                    add_child_window(tag=tag.inve.window(), width=sz.Inve.w, height=sz.Inve.h, border=True, no_scrollbar=True)
            with group(horizontal=False):
                add_child_window(tag=tag.block.window(), width=sz.Block.w, height=sz.Block.h, border=True, no_scrollbar=True)
                add_child_window(tag=tag.wallet.window(), width=sz.Wallet.w, height=sz.Wallet.h, border=True, no_scrollbar=True)

def c_Wallet():
    with group(parent=tag.wallet.window()):
        with group(horizontal=True):
            for coin in Rules.l.Coins:
                with group(horizontal=True):
                    add_button(label=coin)
                    add_text("", color=Coler.Item.M, tag=tag.wallet.val(coin))

def c_Core():
    max_w=sz.Core.w-16
    with group(parent=tag.core.window()):
        add_button(label="Character info", enabled=False, width=max_w, height = sz.Header.A.h)
        with group(horizontal=True):
            add_button(label="Level", enabled=False, width=50)
            add_button(label="<", user_data=["mod_Level", -1], callback=q.cbh)
            add_button(label="", width=25, tag=tag.core.val.level())
            add_button(label=">", user_data=["mod_Level", 1], callback=q.cbh)
            add_button(label="", enabled=False, width=55, tag=tag.core.val.pb())
        
        h_Core_Row("Race", tag.core.select.r(), "mod_Race", max_w)
        h_Core_Row("Subrace", tag.core.select.sr(), "mod_Subrace", max_w)
        h_Core_Row("Class", tag.core.select.c(), "mod_Class", max_w)
        h_Core_Row("Subclass", tag.core.select.sc(), "mod_Subclass", max_w)
        h_Core_Row("Background", tag.core.select.bg(), "mod_Background", max_w)

def c_Atr():
    with group(parent=tag.atr.window()):
        max_w=sz.Atr.w-16
        add_button(label="Attributes", enabled=False, width=max_w, height=sz.Header.A.h)
        for stat in Rules.l.Atr:
            h_Atr_Row(stat)

def c_Health():
    btn_w = sz.Btn.S.w
    with group(parent=tag.health.window()):
        max_w=sz.Health.w-16
        max_h=sz.Health.h-15
        add_button(label="Health", enabled=False, width=max_w, height=sz.Header.A.h)
        with group(horizontal=False):
            with group(horizontal=True):
                add_button(label="+", width=btn_w, user_data=["mod_HP", 1], callback=q.cbh)
                add_button(label="CUR / MAX", enabled=False, width=max_w-108, tag=tag.health.label())
                add_button(label="TEMP", enabled=False, width=max_w-150)
                add_button(label="+", width=btn_w, user_data=["mod_Temp", 1], callback=q.cbh)
            with group(horizontal=True):
                add_button(label="-", width=btn_w, user_data=["mod_HP", -1], callback=q.cbh)
                add_button(label="", enabled=False, width=max_w-108, tag=tag.health.val.hp())
                add_button(label="", enabled=False, width=max_w-150, tag=tag.health.val.temp())
                add_button(label="-", width=btn_w, user_data=["mod_Temp", -1], callback=q.cbh)
    with popup(tag.health.label(), mousebutton=mvMouseButton_Left):
        add_button(label="Max", width=sz.Btn.L.w)
        add_input_int(default_value=0, width=90, user_data=["mod_Base_HP"], callback=q.cbh, tag=tag.health.val.max())

def c_Skills():
    max_w=sz.Skill.w-16
    max_h=sz.Skill.h-15
    with group(parent=tag.skill.window()):
        add_button(label="Skills", enabled=False, width=max_w, height=sz.Header.A.h)
        for skill in Rules.l.Skill:
            h_Skill_Row(skill)

def c_Init():
    h_Stat_Window("Init", tag.init, ["Dex", "Race", "Class", "Feat"])
                
def c_Armor(): 
    h_Stat_Window("AC", tag.ac, ["Base", "Dex", "Shield"])
                
def c_Vision(): 
    h_Stat_Window("Vision", tag.vision, ["Dark", "Blind", "Tremor", "Tru"])

def c_Speed(): 
    h_Stat_Window("Speed", tag.speed, ["Walk", "Climb", "Swim", "Fly", "Burrow"])

def c_Conditions(): 
    with group(parent=tag.cond.window()):
        add_button(label="Conditions", enabled=False, width=sz.Header.B.w-72, height=26, tag=tag.cond.label())
    with popup(tag.cond.label(), mousebutton=mvMouseButton_Left):
        with child_window(auto_resize_x=True, auto_resize_y=True, border=True):
            for i in Rules.l.Condition:
                add_selectable(label=i, default_value=False, user_data=["Condition", i], callback=q.cbh, tag=tag.cond.toggle(i))
    with tooltip(tag.cond.label()):
        with child_window(auto_resize_x=True, auto_resize_y=True, border=True):
            for i in Rules.l.Condition:
                add_text(i, color=Coler.Text, tag=tag.cond.text(i))

def c_Rest(): 
    with group(parent=tag.rest.window()):
        add_button(label="Short Rest", width=sz.Header.B.w-72, height=30, user_data=["Rest", "Short"], callback=q.cbh, tag=tag.rest.button.short())
        add_button(label="Long Rest", width=sz.Header.B.w-72, height=30, user_data=["Rest", "Long"], callback=q.cbh, tag=tag.rest.button.long())

def c_Buffer():
    pass

def c_Prof(): 
    max_w = sz.Prof.w - 16
    max_h = sz.Prof.h - 15
    btn_w = max_w - 101
    with group(parent=tag.prof.window()):
        add_button(label="Proficiencies", enabled=False, width=max_w, height=sz.Header.A.h)
        with group(horizontal=True):
            add_button(label="Weapons", width=btn_w, tag=tag.prof.label.weapon())
            add_button(label="Armor", width=btn_w, tag=tag.prof.label.armor())
        with group(horizontal=True):
            add_button(label="Tools", width=btn_w, tag=tag.prof.label.tool())
            add_button(label="Languages", width=btn_w, tag=tag.prof.label.lang())

def h_Brand(name, width, index):
    parent_tag = tag.brand.char.group(str(index))
    label_t = tag.brand.label(name)
    input_t = tag.brand.input(name)
    text_t = tag.brand.text(name)

    with group(parent=parent_tag):
        add_button(label=name, width=width, tag=label_t)

        with popup(label_t, mousebutton=mvMouseButton_Left):
            add_input_text(default_value="", on_enter=True, user_data=["Brand", name], callback=q.cbh, tag=input_t)
        with tooltip(label_t):
            add_text("", tag=text_t, wrap=400)

def c_Brand():
    max_w = sz.Char.w - 16
    btn_w = max_w - 101
    
    with group(parent=tag.brand.window()):
        add_button(label="Characteristics", enabled=False, width=max_w, height=sz.Header.A.h, tag=tag.brand.char.label())
        
        l_ref = [1,1,2,2]
        with group(horizontal=True, tag=tag.brand.char.group(str(1))): pass
        with group(horizontal=True, tag=tag.brand.char.group(str(2))): pass
        for i, name in enumerate(Rules.l.Brand):
            h_Brand(name, btn_w, l_ref[i])
    h_Char()

def c_Block(): 
    w1 = sz.Block.w - 16
    w2 = w1 - 16
    h1 = sz.Block.h - 40
    h2 = h1 - 15
    with group(parent=tag.block.window()):
        with tab_bar(tag=tag.block.tabbar()):
            with tab(label="Features/Traits"):
                with child_window(width=w1, height=h1, border=True):
                    ####
                    add_separator(label="Race")
                    with child_window(auto_resize_y=True, width=w2, border=True, tag=tag.block.r.asi()):
                        with group(horizontal=True):
                            add_text("Ability Score Increase: +1/+2", color=Coler.Header.G)
                            add_combo(items=Rules.l.Atr, default_value="", width=50, no_arrow_button=True, user_data=["Race Asi", 0], callback=q.cbh, tag=tag.block.r.asi.select.asi_0())
                            add_combo(items=Rules.l.Atr, default_value="", width=50, no_arrow_button=True, user_data=["Race Asi", 1], callback=q.cbh, tag=tag.block.r.asi.select.asi_1())
                            add_button(label="Clear", enabled=True, width=50, user_data=["Race Asi", "Clear"], callback=q.cbh, tag=tag.block.r.asi.button.clear())
                    add_child_window(auto_resize_y=True, width=w2, border=True, tag=tag.block.r.feature())
                    ####
                    add_separator(label="Class")
                    add_child_window(auto_resize_y=True, width=w2, border=True, tag=tag.block.c.skill())
                    add_child_window(auto_resize_y=True, width=w2, border=True, tag=tag.block.c.feature())
                    ###
                    add_separator(label="Feat")
                    with child_window(auto_resize_y=True, width=w2, border=False):
                        with collapsing_header(label="Milestones"):
                            add_child_window(auto_resize_y=True, width=w2, border=True, tag=tag.block.m.panel())
                    add_child_window(auto_resize_y=True, width=w2, border=True, tag=tag.block.m.feature())
                    ####
                    add_separator(label="Background")
                    add_child_window(auto_resize_y=True, width=w2, border=True, tag=tag.block.b.panel())
                    add_child_window(auto_resize_y=True, width=w2, border=True, tag=tag.block.b.feature())
                    ####
            with tab(label="Actions"):
                with child_window(auto_resize_x=True, auto_resize_y=True, border=True):
                    with child_window(auto_resize_y=True, width=w2, border=True, tag=tag.block.actions.window()):
                        add_separator(label="Weapons")

def c_Block_Actions(): 
    with group(parent=tag.block.actions.window()):
        with table(header_row=True, row_background=False, borders_innerH=True, borders_outerH=True, borders_innerV=True, resizable=True,borders_outerV=True):
            add_table_column(label="Weapon", width_stretch=True, init_width_or_weight=0)
            add_table_column(label="Range", width_stretch=True, init_width_or_weight=0)
            add_table_column(label="Hit", width_stretch=True, init_width_or_weight=0)
            add_table_column(label="Damage", width_stretch=True, init_width_or_weight=0)
            add_table_column(label="Type", width_stretch=True, init_width_or_weight=0)
            add_table_column(label="Notes", width_stretch=True, init_width_or_weight=0)
            for i in range(2):
                with table_row():
                    for j in Rules.l.Weapon_Atr:
                        add_table_cell(tag=tag.block.actions.cell(j,i))
    
def c_Inventory(): 
    h=sz.Inve.h
    with group(parent=tag.inve.window()):
        with tab_bar():
            with tab(label="Closet"):
                add_child_window(height=h-28, border=True, no_scrollbar=True, tag=tag.closet.window())
            with tab(label="Backpack"):
                add_child_window(height=h-80, border=True, no_scrollbar=True, tag=tag.backpack.window())
                add_child_window(height=h-294, border=True, tag=tag.backpack.window.totals())
            with tab(label="Bazaar"):
                add_child_window(height=h-26, border=True, no_scrollbar=True, tag=tag.bazaar.window())

def c_Inventory_Backpack(): 
    with group(parent=tag.backpack.window()):
        with table(header_row=True, row_background=False, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, resizable=True, tag=tag.backpack.table()):
            add_table_column(label="Item", width_stretch=True, init_width_or_weight=0)
            add_table_column(label="Slot", width_stretch=True, init_width_or_weight=0)
            add_table_column(label="QTY", width_stretch=True, init_width_or_weight=0)
            add_table_column(label="Weight", width_stretch=True, init_width_or_weight=0)
            add_table_column(label="Cost", width_stretch=True, init_width_or_weight=0)

def c_Inventory_Bazaar(): 
    with group(parent=tag.bazaar.window()):
        with tab_bar():
            for equipment_type in Rules.l.Equip_Type:
                with tab(label=equipment_type):
                    with tab_bar():
                        for rarity in range(5):
                            rank = Rules.fRarity(rarity)
                            with tab(label=rank):
                                add_child_window(height=sz.Inve.h - 85, border=True, no_scrollbar=True, tag=tag.bazaar.window(equipment_type, rank))

def c_Inventory_Closet(): 
    btn_w = 98
    left_slots = ["Face", "Throat", "Body", "Hands", "Waist", "Feet", "Hand_1"]
    right_slots = ["Head", "Shoulders", "Armor", "Arms", "Ring_1", "Ring_2", "Hand_2"]
    
    with group(parent=tag.closet.window()):
        with group(horizontal=False):
            with group(horizontal=True):
                # Left Collumn
                with group(horizontal=False):
                    for slot in left_slots:
                        with group(horizontal=True):
                            add_image_button(tag.closet.icon(slot), callback=q.cbh, user_data=["Closet", slot, "Clear"], tag=tag.closet.img(slot))
                            with child_window(auto_resize_x=True, auto_resize_y=True, border=True, no_scrollbar=True):
                                add_combo(width=btn_w, no_arrow_button=True, user_data=["Closet", slot, "Modify"], callback=q.cbh, tag=tag.closet.select(slot))
                
                # Center Figure
                add_image(tag.closet.icon.figure())
                
                # Right Collumn
                with group(horizontal=False):
                    for slot in right_slots:
                        with group(horizontal=True):
                            with child_window(auto_resize_x=True, auto_resize_y=True, border=True, no_scrollbar=True):
                                add_combo(width=btn_w, no_arrow_button=True, user_data=["Closet", slot, "Modify"], callback=q.cbh, tag=tag.closet.select(slot))
                            add_image_button(tag.closet.icon(slot), callback=q.cbh, user_data=["Closet", slot, "Clear"], tag=tag.closet.img(slot))

def ui_start():
    Load_Icons()
    c_Skeleton()
    c_Core()
    c_Health()
    c_Prof()
    c_Brand()
    c_Buffer()
    c_Atr()
    c_Armor()
    c_Init()
    c_Vision()
    c_Speed()
    c_Conditions()
    c_Rest()
    c_Skills()
    c_Block()
    c_Block_Actions()
    c_Inventory()
    c_Inventory_Backpack()
    c_Inventory_Bazaar()
    c_Inventory_Closet()
    c_Wallet()