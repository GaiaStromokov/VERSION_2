import json, copy
from dataclasses import dataclass
from typing import List, Optional
from Globals.Pathing import get_path

@dataclass
class Item:
    id: str
    base_name: str
    Tier: int
    attributes: dict
    def __getattr__(self, name): return self.attributes.get(name)
    def __repr__(self): return f"<{self.id}>"

class ItemLibrary:
    def __init__(self):
        self.registry = {}
        self._load_items()

    def _load_items(self):
        with open(get_path("dist", "item_file.json"), encoding="utf-8") as f: data = json.load(f)
        for base, attrs in data.items():
            for Tier in attrs.get("Rarity", [0]): self._create_variant(base, attrs, Tier)

    def _create_variant(self, base, attrs, Tier):
        n = copy.deepcopy(attrs); n['Tier'] = Tier
        if n.get("Slot") == "Weapon": n["Damage"]["Hit"] += Tier; n["Damage"]["Dam"] += Tier
        elif n.get("Slot") == "Armor": n["AC"] += Tier
        
        id = base if Tier == 0 else f"{base}_{Tier}"
        self.registry[id] = Item(id, base, Tier, n)

    def get(self, iid) -> Optional[Item]: return self.registry.get(iid)

    def _query(self, **kwargs) -> List[Item]:
        matches = []
        for i in self.registry.values():
            match = True
            for k, v in kwargs.items():
                if k in {'id', 'base_name', 'Tier'}:
                    if getattr(i, k) != v: match = False; break
                else:
                    a = i.attributes.get(k)
                    if isinstance(a, list): 
                        if v not in a: match = False; break
                    elif a != v: match = False; break
            if match: matches.append(i)
        return matches

    def filter(self, **kwargs) -> List[str]: return [i.id for i in self._query(**kwargs)]
    def search(self, **kwargs) -> List[Item]: return self._query(**kwargs)
    
    @property
    def BSW(self): return self.filter(Slot="Weapon", Cat="Simple", Tier=0)
    @property
    def BMW(self): return self.filter(Slot="Weapon", Cat="Martial", Tier=0)
    @property
    def BAW(self): return self.filter(Slot="Weapon", Cat="Simple", Tier=0) + self.filter(Slot="Weapon", Cat="Martial", Tier=0)
    @property
    def BAA(self): return self.filter(Slot="Armor", Tier=0)
    