import yaml
import os
from pathlib import Path

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        # Assumes running from root of project or strict relative path
        base_path = Path(__file__).resolve().parent.parent.parent
        config_path = base_path / "config" / "config.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found at {config_path}")

        with open(config_path, "r") as f:
            self.settings = yaml.safe_load(f)
        
        self.base_path = base_path

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.settings
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

# Global instance
config = Config()
