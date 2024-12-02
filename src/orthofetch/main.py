import click
import subprocess
import asyncio
from pathlib import Path
from rich.console import Console
from rich.layout import Layout
from rich.text import Text
from rich.console import Group
from typing import List

from orthofetch.api.bible_api import OrthoCalAPI, SystemInfo, OrthodoxData, DisplayData

console = Console()

def parse_system_info(raw_info: List[str]) -> SystemInfo:
    """Parse fastfetch output into structured data"""
    system = {"hostname": "", "cpu": "", "gpus": []}
    
    for line in raw_info:
        if "@" in line:
            system["hostname"] = line.strip()
        elif "CPU" in line:
            system["cpu"] = line.replace("CPU", "").strip()
        elif "GPU" in line:
            system["gpus"].append(line.replace("GPU", "").strip())
    
    return SystemInfo(
        hostname=system["hostname"],
        cpu=system["cpu"],
        gpus=system["gpus"]
    )

def collect_system_info() -> SystemInfo:
    """Collect system information from fastfetch"""
    try:
        result = subprocess.run(
            ['fastfetch', '-l', 'none', '-s', 'title:time:cpu:gpu'],
            capture_output=True,
            text=True,
            check=True
        )
        return parse_system_info(result.stdout.strip().split('\n'))
    except (subprocess.CalledProcessError, FileNotFoundError):
        return SystemInfo("Unknown", "Unknown", [])

async def display_content(verse_only: bool, saints_only: bool, config: dict):
    try:
        # Collect all data first
        system_info = collect_system_info()
        api = OrthoCalAPI(config)
        orthodox_data = await api.get_daily_content()
        
        # Load cross ASCII art
        cross_path = Path(__file__).parent / 'calvary_cross.txt'
        with open(cross_path) as f:
            cross_art = f.read()
        
        # Create the formatted display
        layout = Layout()
        
        # Left column with cross
        left_column = Layout(Text(cross_art, style="yellow"), size=30)
        
        # Right column with all text content
        right_content = []
        
        # System info at top
        right_content.extend([
            Text(system_info.hostname, style="bold cyan"),
            Text(f"CPU: {system_info.cpu}", style="cyan"),
            *[Text(f"GPU: {gpu}", style="cyan") for gpu in system_info.gpus],
            Text("")  # Spacing
        ])
        
        # Orthodox content
        right_content.extend([
            Text(orthodox_data.date, style="bold yellow"),
            Text(orthodox_data.title, style="italic"),
            Text("")  # Spacing
        ])
        
        if not saints_only and orthodox_data.readings:
            right_content.append(Text("Scripture Readings", style="bold green"))
            right_content.extend([Text(reading, style="green") for reading in orthodox_data.readings])
            right_content.append(Text(""))  # Spacing
        
        if not verse_only and orthodox_data.saints:
            right_content.append(Text("Commemorations", style="bold red"))
            right_content.extend([Text(saint, style="red") for saint in orthodox_data.saints])
        
        right_column = Layout(Group(*right_content))
        
        # Combine columns
        layout.split_row(left_column, right_column)
        
        # Calculate content height and print
        content_height = len(right_content)
        console.print(layout, height=content_height, crop=True)
                
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@click.command()
@click.option('--verse-only', is_flag=True, help='Show only Bible verse')
@click.option('--saints-only', is_flag=True, help='Show only saints')
@click.option('--no-system', is_flag=True, help='Skip system information')
def main(verse_only, saints_only, no_system):
    """Orthodox Christian system fetch tool"""
    config = {'calendar_type': 'new'}
    asyncio.run(display_content(verse_only, saints_only, config))

if __name__ == '__main__':
    main()