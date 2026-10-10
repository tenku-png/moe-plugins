import math

from base_plugin import BasePlugin
from moegram.composer import ComposerEffects
from ui.settings import Divider, Header, Selector, Switch

__id__ = "typing_fx"
__name__ = "Typing Effects"
__author__ = "@tenku_png"
__version__ = "1.3.0"

MOTIONS = ("pop", "drop", "zoom", "spin")
CURVES = ("auto", "smooth", "linear", "cubic", "back", "elastic", "bounce")
__moegram_api_version__ = "1"


class TypingFX(BasePlugin):
    def on_plugin_load(self):
        for old, key, choices in (("speed", "speed_choice", (0.65, 1.0, 1.6)),
                                  ("intensity", "intensity_choice", (0.5, 1.0, 1.6))):
            if self.get_setting(key) is None:
                try:
                    value = float(self.get_setting(old, "1.0"))
                    if not math.isfinite(value):
                        raise ValueError("Invalid legacy value")
                    index = min(range(3), key=lambda i: abs(choices[i] - value))
                except (TypeError, ValueError):
                    index = 1
                self.set_setting(key, index)
        self.apply_effects()

    def choice(self, key, default, count=3):
        value = self.get_setting(key, default)
        return value if type(value) is int and 0 <= value < count else default

    def apply_effects(self, value=None):
        self.set_composer_effects(ComposerEffects(
            insertion=MOTIONS[self.choice("motion", 0, len(MOTIONS))]
            if self.get_setting("insert", True) else "none",
            deletion=("scatter", "dust")[self.choice("shatter", 1, 2)]
            if self.get_setting("delete", True) else "none",
            caret="smooth" if self.get_setting("cursor", True) else "none",
            send="fade_out" if self.get_setting("send", True) else "none",
            edit="soft" if self.get_setting("insert", True) else "none",
            speed=(0.65, 1.0, 1.6)[self.choice("speed_choice", 1)],
            intensity=(0.5, 1.0, 1.6)[self.choice("intensity_choice", 1)],
            style=("soft", "pop", "bouncy")[self.choice("style", 1)],
            curve=CURVES[self.choice("curve", 0, len(CURVES))],
        ))

    def create_settings(self):
        return [
            Header("Effects"),
            Switch("insert", "Insert animation", True, on_change=self.apply_effects),
            Switch("delete", "Delete animation", True, on_change=self.apply_effects),
            Switch("cursor", "Smooth cursor", True, on_change=self.apply_effects),
            Switch("send", "Send animation", True, on_change=self.apply_effects),
            Divider(),
            Header("Appearance"),
            Selector("style", "Effect style", 1, ["Soft", "Pop", "Bouncy"], on_change=self.apply_effects),
            Selector("motion", "Letters", 0, ["Pop", "Drop", "Zoom", "Spin"], on_change=self.apply_effects),
            Selector("shatter", "Deleted letters", 1, ["Fly away", "Dust"], on_change=self.apply_effects),
            Selector("curve", "Curve", 0, ["Auto", "Smooth", "Linear", "Cubic", "Back", "Elastic", "Bounce"],
                     on_change=self.apply_effects),
            Selector("speed_choice", "Speed", 1, ["Slow", "Normal", "Fast"], on_change=self.apply_effects),
            Selector("intensity_choice", "Intensity", 1, ["Soft", "Normal", "Strong"], on_change=self.apply_effects),
        ]
