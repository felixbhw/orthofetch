from rich.text import Text
from .base import BasePreset, PresetConfig

class EpistlePreset(BasePreset):
    name = "epistle"
    description = "Shows system time and full epistle reading"
    config = PresetConfig(
        show_system=True,
        show_date=True,
        show_readings=True,
        show_saints=False,  # Don't show saints
        show_verses=True,
        system_fields=["hostname", "uptime"]
    )

    def format_content(self, system_info, orthodox_data):
        content = []
        
        # Minimal system info
        if self.config.show_system:
            content.extend([
                Text(system_info.hostname, style="bold cyan"),
                Text("")
            ])
        
        # Date and title
        if self.config.show_date:
            content.extend([
                Text(orthodox_data.date, style="bold yellow"),
                Text(orthodox_data.title, style="italic"),
                Text("")
            ])
        
        # Only show first reading (epistle) with full verse
        if self.config.show_readings and orthodox_data.readings:
            content.append(Text("Epistle Reading", style="bold green"))
            first_reading = orthodox_data.readings[0]
            content.append(Text(first_reading.display, style="bold green"))
            content.append(Text(""))  # Spacing
            
            # Add the full verse content
            verse_text = " ".join(verse.content for verse in first_reading.passage)
            content.append(Text(verse_text, style="green"))
            content.append(Text(""))
        
        return content
