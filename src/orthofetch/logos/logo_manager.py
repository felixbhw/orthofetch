import os
from pathlib import Path

class LogoManager:
    def __init__(self, logo_dir: Path):
        self.logo_dir = logo_dir

    def list_logos(self):
        """List all available logo files."""
        return [f.stem for f in self.logo_dir.glob("*.txt")]

    def load_logo(self, logo_name: str) -> str:
        """Load the specified logo file."""
        logo_path = self.logo_dir / f"{logo_name}.txt"
        if not logo_path.exists():
            raise FileNotFoundError(f"Logo '{logo_name}' not found.")
        with open(logo_path, 'r') as file:
            return file.read()