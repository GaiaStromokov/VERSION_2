from box import Box
from Functions.Pathing import get_path
import json

def load_json(path, file):
    with open(get_path(path, f"{file}.json"), "r") as f:
        return json.load(f)
    
    
class t_Speed:
    Walk = 0
    Climb = 0
    Swim = 0
    Fly = 0
    Burrow = 0

class t_Vision:
    Dark = 0
    Blind = 0
    Tremor = 0
    Tru = 0

class t_Prof:
    Armor = []
    Weapon = []
    Tool = []
    Lang = []
    Skill = []

class t_Combat:
    HD = 0
    HP = 0
    Initiative = 0

class t_Save:
    STR = False
    DEX = False
    CON = False
    INT = False
    WIS = False
    CHA = False

class t_SkillOpt:
    nSelect = 0
    Options = []

class template_Race:
    def __init__(self):
        self.Speed = t_Speed()
        self.Vision = t_Vision()
        self.Prof = t_Prof()
        self.Combat = t_Combat()
        self.Features = []
        self.Caster = None

class template_Class:
    def __init__(self):
        self.Prof = t_Prof()
        self.Skill = t_SkillOpt()
        self.Combat = t_Combat()
        self.Saving_Throw = t_Save()
        self.Features = []