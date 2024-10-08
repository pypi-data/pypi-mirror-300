# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.

from __future__ import annotations

import os
from typing import Optional

from . import ConfigurationProvider
from .abstractions import ConfigurationPath, IConfigurationBuilder, IConfigurationProvider, IConfigurationSource

class EnvironmentVariablesConfigurationProvider(ConfigurationProvider):
    MY_SQL_SERVER_PREFIX: str = "MYSQLCONNSTR_"
    SQL_AZURE_SERVER_PREFIX: str = "SQLAZURECONNSTR_"
    SQL_SERVER_PREFIX: str = "SQLCONNSTR_"
    CUSTOM_CONNECTION_STRING_PREFIX: str = "CUSTOMCONNSTR_"

    _prefix: str
    _normalized_prefix: str

    def __init__(self, prefix: Optional[str] = None):
        """Initializes a new instance."""
        super().__init__()
        self._prefix = ""
        self._normalized_prefix = ""

        if prefix:
            self._prefix = prefix
            self._normalized_prefix = EnvironmentVariablesConfigurationProvider.normalize(prefix)

    def load(self) -> None:
        data: dict[str, Optional[str]] = dict()

        key: str
        value: Optional[str]
        for key, value in os.environ.items():
            transformed_key = key.casefold()
            if transformed_key.startswith(EnvironmentVariablesConfigurationProvider.MY_SQL_SERVER_PREFIX.casefold()):
                self.handle_matched_connection_string_prefix(data, EnvironmentVariablesConfigurationProvider.MY_SQL_SERVER_PREFIX, "MySql.Data.MySqlClient", key, value)
            elif transformed_key.startswith(EnvironmentVariablesConfigurationProvider.SQL_AZURE_SERVER_PREFIX.casefold()):
                self.handle_matched_connection_string_prefix(data, EnvironmentVariablesConfigurationProvider.SQL_AZURE_SERVER_PREFIX, "System.Data.SqlClient", key, value)
            elif transformed_key.startswith(EnvironmentVariablesConfigurationProvider.SQL_SERVER_PREFIX.casefold()):
                self.handle_matched_connection_string_prefix(data, EnvironmentVariablesConfigurationProvider.SQL_SERVER_PREFIX, "System.Data.SqlClient", key, value)
            elif transformed_key.startswith(EnvironmentVariablesConfigurationProvider.CUSTOM_CONNECTION_STRING_PREFIX.casefold()):
                self.handle_matched_connection_string_prefix(data, EnvironmentVariablesConfigurationProvider.CUSTOM_CONNECTION_STRING_PREFIX, None, key, value)
            else:
                self.add_if_normalized_key_matches_prefix(data, EnvironmentVariablesConfigurationProvider.normalize(key), value)

        self.data = data

    def handle_matched_connection_string_prefix(self, data: dict[str, Optional[str]], connection_string_prefix: str, provider: Optional[str], full_key: str, value: Optional[str]) -> None:
        normalized_key_without_connection_string_prefix: str = self.normalize(full_key[len(connection_string_prefix):])

        self.add_if_normalized_key_matches_prefix(data, f"ConnectionStrings:{normalized_key_without_connection_string_prefix}", value)
        if provider is not None:
            self.add_if_normalized_key_matches_prefix(data, f"ConnectionStrings:{normalized_key_without_connection_string_prefix}_ProviderName", provider)

    def add_if_normalized_key_matches_prefix(self, data: dict[str, Optional[str]], normalized_key: str, value: Optional[str]) -> None:
        if normalized_key.casefold().startswith(self._normalized_prefix.casefold()):
            data[normalized_key[len(self._normalized_prefix):]] = value

    @staticmethod
    def normalize(key: str) -> str:
        return key.replace("__", ConfigurationPath.KEY_DELIMITER)
    
class EnvironmentVariablesConfigurationSource(IConfigurationSource):
    """Represents environment variables as an IConfigurationSource."""
    prefix: Optional[str]

    def __init__(self):
        self.prefix = None

    def build(self, builder: IConfigurationBuilder) -> IConfigurationProvider:
        """Builds the EnvironmentVariablesConfigurationProvider for this source."""
        return EnvironmentVariablesConfigurationProvider(self.prefix)

def _add_environment_variables(self, prefix: Optional[str] = None) -> IConfigurationBuilder:
    """Adds an IConfigurationProvider that reads configuration values from environment variables."""
    if prefix:
        self.add(EnvironmentVariablesConfigurationSource(prefix))
    else:
        self.add(EnvironmentVariablesConfigurationSource())

    return self

IConfigurationBuilder.add_environment_variables = _add_environment_variables