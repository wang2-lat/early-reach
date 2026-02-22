import json
from pathlib import Path
from typing import Optional, List
from models import Product, Launch


class LaunchTracker:
    def __init__(self, data_dir: str = ".early-reach"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.product_file = self.data_dir / "product.json"
        self.launches_file = self.data_dir / "launches.json"
    
    def save_product(self, product: Product):
        with open(self.product_file, "w") as f:
            json.dump(product.model_dump(mode="json"), f, indent=2, default=str)
    
    def load_product(self) -> Optional[Product]:
        if not self.product_file.exists():
            return None
        with open(self.product_file, "r") as f:
            data = json.load(f)
            return Product(**data)
    
    def add_launch(self, launch: Launch):
        launches = self.get_launches()
        launches.append(launch)
        with open(self.launches_file, "w") as f:
            json.dump([l.model_dump(mode="json") for l in launches], f, indent=2, default=str)
    
    def get_launches(self) -> List[Launch]:
        if not self.launches_file.exists():
            return []
        with open(self.launches_file, "r") as f:
            data = json.load(f)
            return [Launch(**item) for item in data]
