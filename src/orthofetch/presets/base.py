from dataclasses import dataclass
from typing import List
from rich.text import Text
from orthofetch.api.bible_api import SystemInfo, OrthodoxData

@dataclass
class PresetConfig:
    """Configuration for how a preset should display information"""
    show_system: bool = True
    show_date: bool = True
    show_readings: bool = True
    show_saints: bool = True
    show_verses: bool = False
    system_fields: List[str] = None

class BasePreset:
    """Base class for all display presets"""
    name: str = "base"
    description: str = "Base preset class"
    config: PresetConfig = PresetConfig()

    def format_content(self, system_info: SystemInfo, orthodox_data: OrthodoxData) -> List[Text]:
        """Format the content according to preset rules"""
        raise NotImplementedError
