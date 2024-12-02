import requests
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SystemInfo:
    hostname: str
    cpu: str
    gpus: List[str]

@dataclass
class OrthodoxData:
    date: str
    title: str
    readings: List[str]
    saints: List[str]

@dataclass
class DisplayData:
    system: SystemInfo
    orthodox: OrthodoxData

class OrthoCalAPI:
    BASE_URL = "https://orthocal.info/api"
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.calendar_type = self.config.get('calendar_type', 'gregorian')
    
    def _get_date_url(self, date: datetime) -> str:
        calendar_endpoint = "gregorian" if self.calendar_type == "new" else "julian"
        return f"{self.BASE_URL}/{calendar_endpoint}/{date.year}/{date.month}/{date.day}/"

    async def get_daily_content(self) -> OrthodoxData:
        try:
            today = datetime.now()
            response = requests.get(self._get_date_url(today))
            response.raise_for_status()
            data = response.json()
            
            readings = []
            for idx in data.get('abbreviated_reading_indices', []):
                reading = data['readings'][idx]
                readings.append(reading['display'])
            
            saints = [story['title'] for story in data.get('stories', [])]
            
            return OrthodoxData(
                date=today.strftime("%A, %B %d, %Y"),
                title=data.get('summary_title', ''),
                readings=readings,
                saints=saints
            )
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch Orthodox calendar data: {str(e)}")