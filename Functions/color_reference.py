

c_h1 = (0, 255, 255)    #cyan
c_h2 = (102, 255, 102)  # Bright green
c_h3 = (255, 102, 178)  # Hot pink
c_h4 = (152, 251, 152)  # Light green
c_h5 = (255, 51, 51)    # Bright red
c_h6 = (255, 255, 102)  # Light yellow
c_h7 = (255, 102, 102)  # Light coral/salmon
c_h8 = (102, 178, 255)  # Light blue
c_h9 = (255, 215, 0)    # Gold
c_h10 = (221, 160, 221) # Plum
c_h11 = (255, 165, 0)   # Orange

c_item_true = (102, 255, 102) #Bright green
c_item_false = (211, 211, 211) #dull grey

c_text = (240, 234, 214) #eggshell white


c_spell_school = {
    "Abjuration": (70, 130, 180),       # Steel blue
    "Conjuration": (160, 82, 45),       # Saddle brown
    "Divination": (147, 112, 219),      # Medium slate blue
    "Enchantment": (219, 112, 147),     # Pale violet red
    "Evocation": (255, 140, 0),         # Dark orange
    "Illusion": (72, 209, 204),         # Medium turquoise
    "Necromancy": (75, 0, 130),         # Indigo
    "Transmutation": (34, 139, 34)      # Forest green
}

c_rarity = {
    "Common": (240, 240, 240),      # Silver
    "Uncommon": (50, 205, 50),      # Lime Green
    "Rare": (65, 105, 225),         # Royal Blue
    "Very Rare": (186, 85, 211),    # Medium Orchid
    "Legendary": (220, 20, 60),     # Crimson
    "Artifact": (255, 215, 0)       # Gold
}

c_damagetype = {
    "Piercing": (220, 20, 60),      # Crimson
    "Bludgeoning": (70, 130, 180),  # Steel Blue
    "Slashing": (255, 140, 0),       # Dark Orange
    "NA": (211, 211, 211) #dull grey
}

def c_weapon_dmg(damage): return (255, max(0, 255 - int(damage * 25.5)), max(0, 255 - int(damage * 25.5)))

def c_weapon_hit(damage): return (max(0, 255 - int(damage * 25.5)), max(0, 255 - int(damage * 25.5)), 255)




Tred="\033[91m"
Tgreen="\033[92m"
Tyellow="\033[93m"
Tblue="\033[94m"
Treset="\033[0m"
