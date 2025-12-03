import json
import os
from pathlib import Path

CONFIG_DIR = os.path.join(Path.home(), ".config", "MSIFanControl")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "PROFILE": 1,
    "AUTO_SPEED": [[0, 40, 48, 56, 64, 72, 80], [0, 48, 56, 64, 72, 79, 86]],
    "ADV_SPEED": [[0, 40, 48, 56, 64, 72, 80], [0, 48, 56, 64, 72, 79, 86]],
    "BASIC_OFFSET": 0,
    "CPU": 1,
    "AUTO_ADV_VALUES": [0xd4, 13, 141],
    "COOLER_BOOSTER_OFF_ON_VALUES": [0x98, 2, 130],
    "CPU_GPU_FAN_SPEED_ADDRESS": [[0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78], [0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f, 0x90]],
    "CPU_GPU_TEMP_ADDRESS": [0x68, 0x80],
    "CPU_GPU_RPM_ADDRESS": [0xc8, 0xca],
    "BATTERY_THRESHOLD_VALUE": 100
}

class ConfigManager:
    def __init__(self):
        self.config = DEFAULT_CONFIG.copy()
        self.ensure_config_dir()
        self.load_config()

    def ensure_config_dir(self):
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
            except json.JSONDecodeError:
                print("Error decoding config file. Using defaults.")

    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key):
        return self.config.get(key, DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
