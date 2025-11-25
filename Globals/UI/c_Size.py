class Define:
    def __init__(self, w, h):
        self.w = w
        self.h = h

class Button:
    S = Define(20, 0)
    M = Define(46, 0)
    L = Define(90, 0)

class Header:
    A = Define(0, 20)
    B = Define(188, 0)
    C = Define(116, 0)

class Atr_Row:
    Label = Define(40, 0)
    Val = Define(30, 0)

class Skill_Row:
    Label = Define(113, 0)
    Mod = Define(30, 0)
    Source = Define(50,0)

class Sizing:
    Max = Define(1350, 880)

    Block = Define(Max.w - 595, Max.h - 114)

    Wrap = 700

    Btn = Button()
    Header = Header()
    
    Atr_Row = Atr_Row()
    Skill_Row = Skill_Row()

    AC = Define(62, 58)
    Atr = Define(132, 174)
    Buffer1 = Define(132, 17)
    Buffer2 = Define(210, 13)
    Char = Define(210, 82)
    Cond = Define(132, 42)
    Core = Define(210, 174)
    Health = Define(210, 82)
    Init = Define(62, 58)
    Inve = Define(552, 352)
    Item = Define(117, 0)
    Prof = Define(210, 82)
    Rest = Define(132, 80)
    Skill = Define(194, 449)
    Speed = Define(62, 58)
    Vision = Define(62, 58)
    Wallet = Define(Max.w - 595, 35)
