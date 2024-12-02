from rich.text import Text
from .base import BasePreset, PresetConfig

class DefaultPreset(BasePreset):
    name = "default"
    description = "Default display with all information"
    config = PresetConfig(
        show_system=True,
        show_date=True,
        show_readings=True,
        show_saints=True,
        show_verses=False
    )

    def format_content(self, system_info, orthodox_data):
        content = []
        
        # System info
        if self.config.show_system:
            content.extend([
                Text(system_info.hostname, style="bold cyan"),
                Text(f"CPU: {system_info.cpu}", style="cyan"),
                *[Text(f"GPU: {gpu}", style="cyan") for gpu in system_info.gpus],
                Text("")
            ])
        
        # Orthodox content
        if self.config.show_date:
            content.extend([
                Text(orthodox_data.date, style="bold yellow"),
                Text(orthodox_data.title, style="italic"),
                Text("")
            ])
        
        if self.config.show_readings:
            content.append(Text("Scripture Readings", style="bold green"))
            for reading in orthodox_data.readings:
                content.append(Text(reading.display, style="bold green"))
                if self.config.show_verses:
                    verse_text = " ".join(verse.content for verse in reading.passage)
                    content.append(Text(verse_text, style="green"))
                content.append(Text(""))  # Spacing
        
        if self.config.show_saints:
            content.append(Text("Commemorations", style="bold red"))
            content.extend([Text(saint, style="red") for saint in orthodox_data.saints])
        
        return content
