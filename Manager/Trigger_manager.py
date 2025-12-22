# import q
# import inspect


# class tgen:
#     def __init__(self, name: str):
#         self.name = name.replace("_", " ")
#         self.tag = name.replace(" ", "_")
        
# def register_event(key):
#     def wrapper(func):
#         func._event_key = key
#         return func
#     return wrapper

# def register_action(key):
#     def wrapper(func):
#         func._action_key = key
#         return func
#     return wrapper

# class Base:
#     def __init__(self, parent):
#         self.parent = parent

# class Actions(Base):
#     @register_action("Ward_Heal")
#     def Ward_Heal(self, name, payload):
#         gen = tgen(name)
#         val = payload[0] * 2
#         self.parent.dbm.CBH.cb_class.Arcane_Ward("Trigger", "None", [gen.tag, val])

# class Events(Base):
#     @register_event("Min_Spell")
#     def Min_Spell(self,name, trig, spell):
#         sdata = q.Grimoir(spell)
#         s_School = sdata["School"]
#         s_Level = sdata["Level"]
        
#         meta = trig["Meta"]
        
#         m_School = meta["School"]
#         m_Level = meta["Level"]
#         m_Action = meta["Action"]

#         if s_School != m_School: return
#         if s_Level < m_Level: return
#         handler = self.parent.m_actions.get(m_Action)
#         if handler:
#             payload = [s_Level]
#             handler(name, payload)

# class bTrigger:
#     def __init__(self, parent):
#         self.dbm = parent
#         self.Events = Events(self)
#         self.Actions = Actions(self)
        
#         self.m_events = {}
#         self.m_actions = {}

#         for _, func in inspect.getmembers(self.Events, inspect.ismethod):
#             if hasattr(func, "_event_key"): self.m_events[func._event_key] = func

#         for _, func in inspect.getmembers(self.Actions, inspect.ismethod):
#             if hasattr(func, "_action_key"): self.m_actions[func._action_key] = func

#     def Fire(self, action, payload):
#         handler = self.m_events.get(action)
#         if not handler: return

#         for name, data in self.dbm.db.Class.Features.items():
#             trig = data.get("Trigger")
#             if trig and trig.get("Type") == action:
#                 handler(name, trig, payload)
