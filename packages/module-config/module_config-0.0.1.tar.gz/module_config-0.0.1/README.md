# ModuleConfig

## Overview

`ModuleConfig` is a Python class designed to facilitate the loading and management of configuration settings for applications. It supports both global and local configurations, allowing for a flexible and organized approach to handling application settings.

## Features

-   Load configurations from JSON and YAML files.
-   Support for both global and module-specific local configurations.
-   Ability to retrieve and set configuration values easily.
-   Default values can be specified for configuration retrieval.

## Requirements

-   Python 3.x
-   `PyYAML` library for handling YAML files (install using `pip install PyYAML`).

## Usage

### Importing the Module

To use the `ModuleConfig` class, import it into your Python script:

```python
from module_config import ModuleConfig
```

### Loading Configuration Files

#### Load Global Configuration

To load a global configuration file (either JSON or YAML):

```python
ModuleConfig.load_global_config('path/to/global_config.json')
```

#### Load Local Configuration for a Module

To load a local configuration for a specific module:

```python
ModuleConfig.load_local_config('module_name', 'path/to/local_config.yaml')
```

### Retrieving Configuration Values

To get a configuration value, use the `get_config` method:

```python
# Retrieve a global config value
value = ModuleConfig.get_config('some_key', default='default_value')

# Retrieve a local config value
value = ModuleConfig.get_config('some_key', module_name='module_name', default='default_value')
```

### Setting Configuration Values

You can set configuration values using the `set_config` method:

```python
# Set a global config value
ModuleConfig.set_config('some_key', 'new_value')

# Set a local config value for a specific module
ModuleConfig.set_config('some_key', 'new_value', module_name='module_name')
```

## Error Handling

-   **FileNotFoundError**: Raised when the specified configuration file does not exist.
-   **ValueError**: Raised when an unsupported configuration format is provided.

## Example

Here's a simple example demonstrating how to use `ModuleConfig`:

```python
# Load global config
ModuleConfig.load_global_config('config/global_config.yaml')

# Load local config for a module
ModuleConfig.load_local_config('module1', 'config/module1_config.json')

# Get configuration values
database_url = ModuleConfig.get_config('database_url')
module_specific_setting = ModuleConfig.get_config('setting_key', module_name='module1', default='default_value')

# Set a configuration value
ModuleConfig.set_config('api_key', 'your_api_key_here')
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
