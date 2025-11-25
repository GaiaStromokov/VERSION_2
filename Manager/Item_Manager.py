import json
from Globals.Pathing import get_path

class Item:
    def __init__(self, name, attributes):
        self.name = name
        for key, value in attributes.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items() if k != "name")
        return f"{self.name}({attrs})"


class ItemSearch:
    def __init__(self, items):
        self.items = items

    def Base(self, category):
        results = self.Slot(0, category)
        return [name.rsplit('_', 1)[0] for name in results]

    def __getattr__(self, attr):
        def wrapper(*args):
            value = args[0] if len(args) == 1 else args[1]
            tier_filter = args[0] if len(args) == 2 else None
            results = []
            for item in self.items.values():
                if tier_filter is not None and getattr(item, 'tier', None) != tier_filter:
                    continue
                v = getattr(item, attr, None)
                if v is not None:
                    if isinstance(v, list) and value in v: results.append(item.name)
                    elif v == value: results.append(item.name)
            return results
        return wrapper

class Mitem:
    def __init__(self):
        self.items = self._load_items()
        self.search = ItemSearch(self.items)

    def _load_items(self):
        filepath = get_path("dist", "item_file.json")
        items_dict = {}
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        for name, attributes in data.items():
            for tier in range(4):
                copy = attributes.copy()
                copy['tier'] = tier
                if copy["Slot"] == "Weapon":
                    copy["Damage"] = copy["Damage"].copy()
                    copy["Damage"]["Hit"] += tier
                    copy["Damage"]["Dam"] += tier
                elif copy["Slot"] == "Armor":
                    copy["AC"] += tier
                item_name = f"{name}_{tier}"
                items_dict[item_name] = Item(item_name, copy)
        return items_dict

    def dItem(self, name):
        return self.items.get(name)
