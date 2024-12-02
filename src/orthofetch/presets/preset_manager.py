from typing import Dict, Type
from .base import BasePreset
from .default import DefaultPreset
from .epistle import EpistlePreset

class PresetManager:
    def __init__(self):
        self._presets: Dict[str, Type[BasePreset]] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register built-in presets"""
        self.register_preset(DefaultPreset)
        self.register_preset(EpistlePreset)

    def register_preset(self, preset_class: Type[BasePreset]):
        """Register a new preset"""
        self._presets[preset_class.name] = preset_class

    def get_preset(self, name: str) -> BasePreset:
        """Get a preset by name"""
        if name not in self._presets:
            raise ValueError(f"Preset '{name}' not found. Available presets: {', '.join(self._presets.keys())}")
        return self._presets[name]()

    def list_presets(self):
        """List all available presets"""
        return [(name, preset.description) for name, preset in self._presets.items()]
