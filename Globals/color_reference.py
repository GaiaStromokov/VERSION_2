class Text:
    Base = (240, 234, 214) # Off-White
    

class Header:
    C = (0, 255, 255)    #cyan
    G = (102, 255, 102)  # Bright green
    HP = (255, 102, 178)  # Hot pink


class Item:
    T = (102, 255, 102) # Light Green (True)
    F = (211, 211, 211) # Light Grey (False)
    G = (0, 255, 0)     # Green
    U = (0, 0, 255)     # Blue
    P = (255, 105, 180) # Pink
    M = (249, 191, 32)  # Money
    

class School:
    Abjuration = (70, 130, 180)    # Steel Blue
    Conjuration = (160, 82, 45)    # Sienna
    Divination = (147, 112, 219)   # Medium Purple
    Enchantment = (219, 112, 147)  # Pale Violet Red
    Evocation = (255, 140, 0)      # Dark Orange
    Illusion = (72, 209, 204)      # Medium Turquoise
    Necromancy = (75, 0, 130)      # Indigo
    Transmutation = (34, 139, 34)  # Forest Green

class Rarity:
    Common = (240, 240, 240)       # Off White
    Uncommon = (50, 205, 50)       # Lime Green
    Rare = (65, 105, 225)          # Royal Blue
    VeryRare = (186, 85, 211)      # Dark Orchid
    Legendary = (220, 20, 60)      # Crimson
    Artifact = (255, 215, 0)       # Gold

class Coler:
    Text = Text.Base
    Header = Header
    Item = Item
    sSchool = School
    iRarity = Rarity
