from rich.text import Text
from .base import BasePreset, PresetConfig

class SystemPreset(BasePreset):
    name = "system"
    description = "Shows full system information with date and saint of the day"
    config = PresetConfig(
        show_system=True,
        show_date=True,
        show_readings=False,
        show_saints=True,
        show_verses=False,
        system_fields=["all"]  # Show all system fields
    )

    def format_content(self, system_info, orthodox_data):
        content = []
        
        if self.config.show_system:
            content.extend([
                Text(system_info.hostname, style="bold cyan"),
                Text(f"OS: {system_info.os}", style="cyan"),
                Text(f"Kernel: {system_info.kernel}", style="cyan"),
                Text(f"DE: {system_info.de}", style="cyan"),
                Text(f"WM: {system_info.wm}", style="cyan"),
                Text(f"Terminal: {system_info.terminal}", style="cyan"),
                Text(f"Shell: {system_info.shell}", style="cyan"),
                Text(f"CPU: {system_info.cpu}", style="cyan"),
                *[Text(f"GPU: {gpu}", style="cyan") for gpu in system_info.gpus],
                Text(f"Memory: {system_info.memory}", style="cyan"),
                Text(f"Uptime: {system_info.uptime}", style="cyan"),
                Text(f"Resolution: {system_info.resolution}", style="cyan"),
                Text(f"Theme: {system_info.theme}", style="cyan"),
                Text(f"Icons: {system_info.icons}", style="cyan"),
                Text(f"Font: {system_info.font}", style="cyan"),
                Text(f"Cursor: {system_info.cursor}", style="cyan"),
                Text("")
            ])
        
        # Date and first saint
        if self.config.show_date:
            content.extend([
                Text(orthodox_data.date, style="bold yellow"),
                Text("")
            ])
        
        if self.config.show_saints and orthodox_data.saints:
            content.extend([
                Text("Saint of the Day", style="bold red"),
                Text(orthodox_data.saints[0], style="red"),  # Show only first saint
                Text("")
            ])
        
        return content