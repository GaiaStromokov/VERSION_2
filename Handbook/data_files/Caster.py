from box import Box
import q
Rules = q.Rules


class Caster_Template:
    def __init__(self, Level):
        self.Level = Level

        self.L_MSL = [0] * 21
        self.L_CA  = [0] * 21
        self.L_SA  = [0] * 21

        self.Abil = ""
        self.List = ""
        self.Book = [[] for _ in range(10)]
        self.Prepared = [[] for _ in range(10)]
        self.PT = "None"

        self.Slot = [[0] * 10 for _ in range(21)]
        self.Casting = {}
        self.Tog = False

    def resolve(self):
        Slot = [[False] * n for n in self.Slot[self.Level]]
        self.Casting = {
            "MSL":  self.L_MSL[self.Level],
            "CA":   self.L_CA[self.Level],
            "SA":   self.L_SA[self.Level],
            "Tog":  self.Tog,
            "Abil": self.Abil,
            "List": self.List,
            "Book": self.Book,
            "Prepared": self.Prepared,
            "PT": self.PT,
            "Slot": Slot
        }


class Empty(Caster_Template):
    def __init__(self, Level):
        super().__init__(Level)
        self.Abil = "None"
        self.List = "None"
        self.PT = "None"
        self.L_MSL = [0] * 21
        self.L_CA  = [0] * 21
        self.L_SA  = [0] * 21
        self.Slot  = [[0] * 10 for _ in range(21)]
        self.Tog = False
        self.resolve()


class Wizard(Caster_Template):
    def __init__(self, Level):
        super().__init__(Level)

        self.Abil = "INT"
        self.List = "Wizard"
        self.PT = "Full"

        self.L_MSL = [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,9,9]
        self.L_CA  = [0,3,3,3,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5]
        self.L_SA  = [0,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44]

        self.Slot = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,2,0,0,0,0,0,0,0,0],
            [0,3,0,0,0,0,0,0,0,0],
            [0,4,2,0,0,0,0,0,0,0],
            [0,4,3,0,0,0,0,0,0,0],
            [0,4,3,2,0,0,0,0,0,0],
            [0,4,3,3,0,0,0,0,0,0],
            [0,4,3,3,1,0,0,0,0,0],
            [0,4,3,3,2,0,0,0,0,0],
            [0,4,3,3,3,1,0,0,0,0],
            [0,4,3,3,3,2,0,0,0,0],
            [0,4,3,3,3,2,1,0,0,0],
            [0,4,3,3,3,2,1,0,0,0],
            [0,4,3,3,3,2,1,1,0,0],
            [0,4,3,3,3,2,1,1,0,0],
            [0,4,3,3,3,2,1,1,1,0],
            [0,4,3,3,3,2,1,1,1,0],
            [0,4,3,3,3,2,1,1,1,1],
            [0,4,3,3,3,3,1,1,1,1],
            [0,4,3,3,3,3,2,1,1,1],
            [0,4,3,3,3,3,2,2,1,1]
        ]
        self.Tog = True
        self.resolve()


class Fighter_Eldritch_Knight(Caster_Template):
    def __init__(self, Level):
        super().__init__(Level)

        self.Abil = "INT"
        self.List = "Wizard"
        self.PT = "None"

        self.L_MSL = [0,0,0,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4]
        self.L_CA  = [0,0,0,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3]
        self.L_SA  = [0,0,0,3,4,4,4,5,6,6,7,8,8,9,10,10,11,11,12,13,13]

        self.Slot = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [2,2,0,0,0,0,0,0,0,0],
            [0,3,0,0,0,0,0,0,0,0],
            [0,3,0,0,0,0,0,0,0,0],
            [0,3,0,0,0,0,0,0,0,0],
            [0,4,2,0,0,0,0,0,0,0],
            [0,4,2,0,0,0,0,0,0,0],
            [0,4,2,0,0,0,0,0,0,0],
            [0,4,3,0,0,0,0,0,0,0],
            [0,4,3,0,0,0,0,0,0,0],
            [0,4,3,0,0,0,0,0,0,0],
            [0,4,3,2,0,0,0,0,0,0],
            [0,4,3,2,0,0,0,0,0,0],
            [0,4,3,2,0,0,0,0,0,0],
            [0,4,3,3,0,0,0,0,0,0],
            [0,4,3,3,0,0,0,0,0,0],
            [0,4,3,3,0,0,0,0,0,0],
            [0,4,3,3,1,0,0,0,0,0],
            [0,4,3,3,1,0,0,0,0,0]
        ]
        self.Tog = True
        self.resolve()


Catalog = {
    "Fighter": {
        "Eldritch_Knight": Fighter_Eldritch_Knight
    },
    "Wizard": {
        "Base": Wizard
    }
}


def get_Caster_Data(main, sub, level):
    if main not in Catalog: return Empty(level)
    group = Catalog[main]
    if sub in group: return group[sub](level)
    if "Base" in group: return group["Base"](level)
    return Empty(level)
