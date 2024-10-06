from dataclasses import dataclass
from typing import Optional

from nema.connectivity import ConnectivityManager


@dataclass
class App:
    global_id: int
    name: str = ""
    description: str = ""
    output_folder: Optional[str] = None

    def download_code(self):
        conn = ConnectivityManager()

        return conn.retrieve_app_code(self.global_id)
