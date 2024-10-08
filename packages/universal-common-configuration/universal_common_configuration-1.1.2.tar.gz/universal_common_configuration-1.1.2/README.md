# universal-common-configuration

A Python library inspired by Microsoft.Extensions.Configuration, providing a flexible configuration system for applications. This library allows you to load configuration data from various sources such as JSON files, environment variables, and user secrets.

## Features

- Load configuration from multiple sources
- Support for JSON configuration files
- Hierarchical configuration structure
- Optional file loading
- Extensible design for adding new configuration sources

## Installation

Install the package from PyPi using pip:

```bash
pip install universal-common-configuration
```

## Usage

### Basic Usage

```python
from universal_common_configuration import ConfigurationBuilder, IConfiguration

# Create a configuration builder
builder = ConfigurationBuilder()

# Add a JSON file to the configuration
builder.add_json_file("config.json")

# Build the configuration
configuration: IConfiguration = builder.build()

# Access configuration values
database_name = configuration["Database:Name"] # or configuration.get_section("Database")["Name"]
port = int(configuration["Server:Port"])
connection_string = configuration.get_connection_string("StorageService") # short for configuration.get_section("ConnectionStrings")["StorageService"]
```

### Working with Optional Files

```python
# Add an optional JSON file
builder.add_json_file("optional_config.json", optional=True)
```

### Combining Multiple Sources
Matched keys in later sources override the same key on earlier sources.

```python
builder.add_json_file("appsettings.json")
      .add_json_file(f"appsettings.{environment}.json", optional=True)
      .add_environment_variables()
      .add_user_secrets()

configuration = builder.build()
```

The various methods extending IConfiguration are monkey patched with the relevant import (eg. import universal_common_configuration.json for add_json_file or add_json_string).