from dearpygui.dearpygui import *
import q, re, math
from colorist import *
Coler = q.Coler
Grimoir = q.Grimoir
class tgen:
    def __init__(self, name: str):
        self.name = name.replace("_", " ")
        self.tag = name.replace(" ", "_")


def gen_abil(name: str):
    an = name
    tn = name.replace(" ", "_")
    return an, tn 

def idel(tag):
    if does_item_exist(tag): delete_item(item=tag, children_only=False)

def icl(tag):
    if does_item_exist(tag): delete_item(item=tag, children_only=True)
    



def item_detail_handler(item):
    data = q.w.dItem(item)

    item_type = data.Slot
    if item_type == "Weapon":
        if "Shield" in data.Cat:
            item_type = "Shield"

    detail_functions = {
        "Weapon": item_detail_weapon,
        "Shield": item_detail_shield,
        "Armor": item_detail_armor,
    }

    if func := detail_functions.get(item_type):
        func(data)


def item_detail_weapon(data):
    with group(horizontal=True):
        if data.get("Reach"):
            add_text("Reach", color=Coler.Header.G)
            add_text(data.Reach, color=Coler.Text)
        if data.get("Range"):
            add_text("Range", color=Coler.Header.G)
            add_text(data.Range, color=Coler.Text)
        add_text("Damage", color=Coler.Header.G)
        add_text(data.Damage, color=Coler.Header.HP)
        # add_text(data.Type, color=c_damagetype[f"{data.Type}"])

    with group(horizontal=True):
        add_text("Prop", color=Coler.Header.G)
        for prop in data.Prop:
            add_text(f"{prop}", color=Coler.Text)
        add_text("Rarity", color=Coler.Header.G)
        # add_text(get.item_rarity(data.Tier), color=c_rarity[f"{get.item_rarity(data.Tier)}"])
        add_text("Weight", color=Coler.Header.G)
        add_text(data.Weight, color=Coler.Text)
        add_text("Cost", color=Coler.Header.G)
        add_text(data.Cost, color=Color.Item.Money)

def item_detail_shield(data):
    with group(horizontal=True):
        add_text("AC", color=Coler.Header.G)
        add_text(data.AC, color=Coler.Text)
        add_text("Rarity", color=Coler.Header.G)
        # add_text(get.item_rarity(data.Tier), color=c_rarity[f"{get.item_rarity(data.Tier)}"])
        add_text("Weight", color=Coler.Header.G)
        add_text(data.Weight, color=Coler.Text)
        add_text("Cost", color=Coler.Header.G)
        add_text(data.Cost, color=Color.Item.Money)

def item_detail_armor(data):
    pass

def spell_detail(spell):
    try: data = Grimoir[spell]
    except (KeyError, AttributeError, TypeError): return 
    with group(horizontal=True):
        add_text("Level", color=Coler.Header.G)
        if data["Level"] == 0: add_text("Cantrip", color=Coler.Text)
        else: add_text(data["Level"], color=Coler.Text)
        add_text("School", color=Coler.Header.G)
        add_text(data["School"], color=getattr(Coler.School, data['School']))
    with group(horizontal=True):
        add_text("Range", color=Coler.Header.G)
        add_text(data["Range"], color=Coler.Text)
        add_text("Components", color=Coler.Header.G)
        add_text(data["Components"], color=Coler.Text)
    with group(horizontal=True):
        add_text("Casting Time", color=Coler.Header.G)
        add_text(data["Casting Time"], color=Coler.Text)
        add_text("Duration", color=Coler.Header.G)
        add_text(data["Duration"], color=Coler.Text)
    with group(horizontal=True):
        if data.get("Ritual"):
            add_text("Ritual", color=Coler.Header.G)
            add_text(data["Ritual"], color=Coler.Text)
        if data.get("Concentration"):
            add_text("Concentration", color=Coler.Header.G)
            add_text(data["Concentration"], color=Coler.Text)
    with group(horizontal=False):
        add_text("Description", color=Coler.Header.G)
        add_text(data["Desc"], color=Coler.Text, wrap=420)

pat = re.compile(r"\{([^{}]+)\}")
def dres(text):
    core = q.dbm.db.Core["Level"]
    Atr = q.dbm.db.Atr
    local = {
        "PB":core.PB,
        "LEVEL":core.Val,
        "STR":Atr["STR"].Mod,
        "DEX":Atr["DEX"].Mod,
        "CON":Atr["CON"].Mod,
        "INT":Atr["INT"].Mod,
        "WIS":Atr["WIS"].Mod,
        "CHA":Atr["CHA"].Mod}
    return pat.sub(lambda m: str(math.ceil(eval(m.group(1), {}, local))), text)