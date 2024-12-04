import click
import subprocess
import asyncio
from pathlib import Path
from rich.console import Console
from rich.layout import Layout
from rich.text import Text
from rich.console import Group
from typing import List

from orthofetch.api.bible_api import OrthoCalAPI, SystemInfo, OrthodoxData
from orthofetch.logos.logo_manager import LogoManager
from orthofetch.presets.preset_manager import PresetManager

console = Console()

def parse_system_info(raw_info: List[str]) -> SystemInfo:
    """Parse fastfetch output into structured data"""
    system = {
        "hostname": "", "cpu": "", "gpus": [], "kernel": "", "os": "",
        "de": "", "wm": "", "terminal": "", "shell": "", "packages": "",
        "memory": "", "uptime": "", "resolution": "", "theme": "",
        "icons": "", "font": "", "cursor": ""
    }
    
    field_mapping = {
        "@": "hostname",
        "CPU": "cpu",
        "GPU": "gpus",
        "Kernel": "kernel",
        "OS": "os",
        "DE": "de",
        "WM": "wm",
        "Terminal": "terminal",
        "Shell": "shell",
        "Packages": "packages",
        "Memory": "memory",
        "Uptime": "uptime",
        "Resolution": "resolution",
        "Theme": "theme",
        "Icons": "icons",
        "Font": "font",
        "Cursor": "cursor"
    }
    
    for line in raw_info:
        for key, field in field_mapping.items():
            if key in line:
                if field == "gpus":
                    system["gpus"].append(line.replace("GPU", "").strip())
                else:
                    system[field] = line.replace(key, "").strip()
    
    return SystemInfo(**system)

def collect_system_info() -> SystemInfo:
    """Collect system information from fastfetch"""
    try:
        result = subprocess.run(
            ['fastfetch', '-l', 'none', '--load-config', 'none', '--structure', 
             'title:kernel:os:de:wm:terminal:shell:packages:memory:cpu:gpu:uptime:resolution:theme:icons:font:cursor'],
            capture_output=True,
            text=True,
            check=True
        )
        return parse_system_info(result.stdout.strip().split('\n'))
    except (subprocess.CalledProcessError, FileNotFoundError):
        return SystemInfo("Unknown", "Unknown", [], "Unknown", "Unknown", "Unknown", 
                        "Unknown", "Unknown", "Unknown", "Unknown", "Unknown", "Unknown",
                        "Unknown", "Unknown", "Unknown", "Unknown", "Unknown")

@click.command()
@click.option('--verse-only', is_flag=True, help='Show only Bible verse')
@click.option('--saints-only', is_flag=True, help='Show only saints')
@click.option('--no-system', is_flag=True, help='Skip system information')
@click.option('--logo', type=click.Choice(['calvary_cross', 'orthodox_cross', 'dove']), 
              default='calvary_cross', help='Select logo to display')
@click.option('--preset', type=click.Choice(['default', 'epistle', 'system']), 
              default='default', help='Select display preset')
def main(verse_only, saints_only, no_system, logo, preset):
    """Orthodox Christian system fetch tool"""
    config = {'calendar_type': 'new'}
    asyncio.run(display_content(verse_only, saints_only, config, logo, preset))

async def display_content(verse_only: bool, saints_only: bool, config: dict, logo: str, preset: str):
    try:
        # Initialize managers
        logo_manager = LogoManager(Path(__file__).parent / 'logos')
        preset_manager = PresetManager()
        
        # Get selected preset
        current_preset = preset_manager.get_preset(preset)
        
        # Load logo
        cross_art = logo_manager.load_logo(logo)
        
        # Collect data
        system_info = collect_system_info()
        api = OrthoCalAPI(config)
        orthodox_data = await api.get_daily_content()
        
        # Format content using preset
        right_content = current_preset.format_content(system_info, orthodox_data)
        
        # Create layout
        layout = Layout()
        layout.split_row(
            Layout(Text(cross_art, style="yellow"), size=30),
            Layout(Group(*right_content))
        )
        
        # Calculate content height considering text wrapping
        logo_height = len(cross_art.split('\n'))
        
        # Calculate wrapped content height
        terminal_width = console.width - 30  # Subtract logo width
        content_height = 0
        for text in right_content:
            # Estimate wrapped lines for each text element
            wrapped_lines = (len(str(text)) // terminal_width) + 1
            content_height += wrapped_lines
        
        # Add small buffer and use maximum height
        display_height = max(logo_height, content_height) + 2
        
        # Print with calculated height
        console.print(layout, height=display_height, crop=False)
                
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

if __name__ == '__main__':
    main()