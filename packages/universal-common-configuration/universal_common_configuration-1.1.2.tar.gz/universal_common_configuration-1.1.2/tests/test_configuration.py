import os
from uuid import uuid4

import pytest

from universal_common_configuration import ConfigurationBuilder, IConfiguration, IConfigurationSection
import universal_common_configuration.environment_variables
import universal_common_configuration.json
import universal_common_configuration.user_secrets

class TestConfiguration:
    def test_create_configuration_environment_variables(self):
        random_string: str = str(uuid4())
        os.environ["TEST"] = random_string
        configuration: IConfiguration = ConfigurationBuilder().add_environment_variables().build()
        assert configuration["TEST"] == random_string

    def test_can_create_sections_from_environment_variables(self):
        random_string: str = str(uuid4())
        os.environ["ConnectionStrings:Database"] = random_string
        configuration: IConfiguration = ConfigurationBuilder().add_environment_variables().build()
        configurationSection: IConfigurationSection = configuration.get_section("ConnectionStrings")
        assert configurationSection is not None
        assert configurationSection["Database"] == random_string
        assert configuration.get_connection_string("Database") == random_string

    def test_non_existent_user_secrets_doesnt_crash(self):
        ConfigurationBuilder().add_user_secrets("asdf").build()

    def test_json_string(self):
        configuration: IConfiguration = ConfigurationBuilder().add_json_string(
            """
            {
                "simple": "asdf",
                "array": [
                    {
                        "Hey": 1,
                        "What": "Who?"
                    }
                ]
            }
            """
        ).build()

        assert configuration is not None
        assert configuration["simple"] == "asdf"
    
        assert configuration["array:0:Hey"] == "1"
        assert configuration["array:0:What"] == "Who?"
        
        assert configuration["nonexistent"] is None
        assert configuration["array:1"] is None
        
        array_section = configuration.get_section("array")
        assert array_section is not None
        assert array_section["0:Hey"] == "1"
        assert array_section["0:What"] == "Who?"
        
        array_children = list(array_section.get_children())
        assert len(array_children) == 1
        assert array_children[0]["Hey"] == "1"
        assert array_children[0]["What"] == "Who?"
        
        assert configuration["array:0:Hey"] == configuration.get_section("array").get_section("0")["Hey"]

    def test_json_file(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        config_path = os.path.join(current_dir, "config.json")
        
        assert os.path.exists(config_path), f"Config file not found at {config_path}"

        configuration: IConfiguration = ConfigurationBuilder().add_json_file(config_path).build()
        assert configuration is not None
        assert configuration["simple"] == "asdf"
    
        assert configuration["array:0:Hey"] == "1"
        assert configuration["array:0:What"] == "Who?"
        
        assert configuration["nonexistent"] is None
        assert configuration["array:1"] is None
        
        array_section = configuration.get_section("array")
        assert array_section is not None
        assert array_section["0:Hey"] == "1"
        assert array_section["0:What"] == "Who?"
        
        array_children = list(array_section.get_children())
        assert len(array_children) == 1
        assert array_children[0]["Hey"] == "1"
        assert array_children[0]["What"] == "Who?"
        
        assert configuration["array:0:Hey"] == configuration.get_section("array").get_section("0")["Hey"]

    def test_json_file_not_optional(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "config.json")
        
        configuration = ConfigurationBuilder().add_json_file(config_path, optional=False).build()
        assert configuration is not None
        assert configuration["simple"] == "asdf"

        with pytest.raises(FileNotFoundError):
            ConfigurationBuilder().add_json_file("non_existent.json", optional=False).build()

    def test_json_file_optional(self):
        configuration = ConfigurationBuilder().add_json_file("non_existent.json", optional=True).build()
        assert configuration is not None
        assert len(list(configuration.get_children())) == 0