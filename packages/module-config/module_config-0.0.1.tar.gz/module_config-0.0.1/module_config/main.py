import os
import json
import yaml
from typing import Dict, Any, Optional

class ModuleConfig:
    _global_config: Dict[str, Any] = {}
    _local_configs: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """Load a configuration file."""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        _, ext = os.path.splitext(config_path.lower())
        with open(config_path, 'r') as file:
            if ext == '.json':
                return json.load(file)
            elif ext in ('.yaml', '.yml'):
                return yaml.safe_load(file)
            else:
                raise ValueError(f"Unsupported config format: {ext}")

    @classmethod
    def load_global_config(cls, config_path: str) -> None:
        """Load a global configuration file"""
        cls._global_config = cls.load_config(config_path)

    @classmethod
    def load_local_config(cls, module_name: str, config_path: str) -> None:
        """Load a local configuration file for a specific module"""
        cls._local_configs[module_name] = cls.load_config(config_path)

    @classmethod
    def get_config(cls, key: str, module_name: Optional[str] = None, default: Optional[Any] = None) -> Any:
        """
        Get a config value. First check local config, then global.
        If the key or module does not exist, return the default value.
        """
        if module_name and module_name in cls._local_configs:
            return cls._local_configs[module_name].get(key, cls._global_config.get(key, default))
        return cls._global_config.get(key, default)

    @classmethod
    def set_config(cls, key: str, value: Any, module_name: Optional[str] = None) -> None:
        """Set a config value. If module_name is provided, set local config, otherwise set global."""
        if module_name:
            if module_name not in cls._local_configs:
                cls._local_configs[module_name] = {}
            cls._local_configs[module_name][key] = value
        else:
            cls._global_config[key] = value

if __name__ == '__main__':
    ModuleConfig.set_config('key1', 'value1', 'module1')
    ModuleConfig.set_config('key1', 'value2')
    print(ModuleConfig.get_config('key1', 'module1'))  # Output: value1
    print(ModuleConfig.get_config('key1'))  # Output: value2