from typing import Callable, Dict, Any, List

class Tag:
    special = {"STR", "DEX", "CON", "INT", "WIS", "CHA", "AC", "HP"}

    def __init__(self):
        self._panel_cache: Dict[str, 'Tag.Tagger'] = {}

    @staticmethod
    def _format_part(part: Any) -> str:
        s = str(part)
        return s.upper() if s.upper() in Tag.special else s.capitalize()

    def __getattr__(self, panel_name: str) -> 'Tag.Tagger':
        if panel_name not in self._panel_cache:
            self._panel_cache[panel_name] = self.Tagger([panel_name], self._format_part)
        return self._panel_cache[panel_name]

    def _traverse_vis(self, tagger_instance: 'Tag.Tagger'):
        if not tagger_instance._next_cache:
            if len(tagger_instance._parts) == 1:
                print(f"Panel: {tagger_instance._parts[0]} (No Suffixes Cached)")
            else:
                print(".".join(tagger_instance._parts))
        else:
            for child_tagger in tagger_instance._next_cache.values():
                self._traverse_vis(child_tagger)

    def Vis(self):
        for tagger_l1 in self._panel_cache.values():
            self._traverse_vis(tagger_l1)

    class Tagger:
        def __init__(self, parts: List[str], formatter: Callable[[Any], str]):
            self._parts: List[str] = parts
            self._format: Callable[[Any], str] = formatter
            self._next_cache: Dict[str, 'Tag.Tagger'] = {}

        def __getattr__(self, suffix: str) -> 'Tag.Tagger':
            if suffix not in self._next_cache:
                new_parts = self._parts + [suffix]
                self._next_cache[suffix] = Tag.Tagger(new_parts, self._format)
            return self._next_cache[suffix]

        def __call__(self, *identifiers: Any) -> str:
            parts: List[str] = [self._format(p) for p in self._parts]
            if identifiers:
                parts.extend(self._format(i) for i in identifiers)
            return "_".join(parts)
