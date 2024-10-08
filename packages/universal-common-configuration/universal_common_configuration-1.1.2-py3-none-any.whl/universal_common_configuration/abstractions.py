# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.

from __future__ import annotations

from typing import Optional

from abc import ABC, abstractmethod
from collections.abc import Iterable

class ConfigurationPath:
    """Utility methods and constants for manipulating Configuration paths"""
    KEY_DELIMITER: str = ":"

    @staticmethod
    def combine(*path_segments: str) -> str:
        """Combines path segments into one path.
        
        :param list[str] path_segments: The path segments to combine.
        :return: The combined path"""
        return ConfigurationPath.KEY_DELIMITER.join(path_segments)

    @staticmethod
    def get_section_key(path: Optional[str]) -> Optional[str]:
        """Extracts the last path segment from the path.
        
        :param str path: The path.
        :return: The last path segment of the path."""
        if not path:
            return path
        
        last_delimiter_index: int = path.rfind(ConfigurationPath.KEY_DELIMITER)
        return path if last_delimiter_index < 0 else path[last_delimiter_index + 1:]
    
    @staticmethod
    def get_parent_path(path: Optional[str]) -> Optional[str]:
        """Extracts the path corresponding to the parent node for a given path.
        
        :param str path: The path.
        :rtype: Optional[str]
        :return: The original path minus the last individual segment found in it. Null if the original path corresponds to a top level node."""
        if not path:
            return None
        
class IComparer(ABC):
    def compare(x: any, y: any) -> int:
        """Compares two objects and returns a value indicating whether one is less than, equal to, or greater than the other."""
        pass

class IConfiguration(ABC):
    @abstractmethod
    def __getitem__(self, key: str) -> str:
        pass

    @abstractmethod
    def __setitem__(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def get_section(self, key: str) -> IConfigurationSection:
        """Gets a configuration sub-section with the specified key.
        
        :param str key: The key of the configuration section."""
        pass

    @abstractmethod
    def get_children(self) -> Iterable[IConfigurationSection]:
        """Gets the immediate descendant configuration sub-sections.
        
        :return: The configuration sub-sections."""
        pass

    def get_connection_string(self, name: str) -> Optional[str]:
        """Shorthand for get_section("ConnectionStrings")[name]."""
        return self.get_section("ConnectionStrings")[name]

class IConfigurationBuilder(ABC):
    @abstractmethod
    def properties(self) -> dict[str, object]:
        pass

    @property
    @abstractmethod
    def sources(self) -> list[IConfigurationSource]:
        pass

    @abstractmethod
    def add(self, source: IConfigurationSource) -> IConfigurationBuilder:
        """Adds a new configuration source.
        
        :param IConfigurationSource source: The configuration source to add."""
        pass

    @abstractmethod
    def build(self) -> IConfigurationRoot:
        """Builds an IConfiguration with keys and values from the set of sources registered in"""
        pass
    
class IConfigurationProvider(ABC):
    """Provides configuration key/values for an application."""
    @abstractmethod
    def try_get(self, key: str) -> tuple[bool, Optional[str]]:
        """Tries to get a configuration value for the specified key.
        
        :param str key: The key.
        :return: True if a value for the specified key was found, otherwise False.
        """
        pass

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        """Sets a configuration value for the specified key.
        
        :param str key: The key.
        :param str value: The value."""
        pass

    @abstractmethod
    def load(self) -> None:
        """Loads configuration values from the source represented by this IConfigurationProvider."""
        pass

    @abstractmethod
    def get_child_keys(self, earlier_keys: Iterable[str], parent_path: str) -> Iterable[str]:
        """Returns the immediate descendant configuration keys for a given parent path based on this IConfigurationProviders data and the set of keys returned by all the preceding IConfigurationProviders.
        
        :param Iterable[str] earlier_keys: The child keys returned by the preceding providers for the same parent path.
        :param str parent_path: The parent path.
        :return: The child keys.
        """
        pass

class IConfigurationRoot(IConfiguration):
    """Represents the root of an IConfiguration hierarchy."""
    @abstractmethod
    def reload(self):
        """Force the configuration values to be reloaded from the underlying IConfigurationProviders."""
        pass
    
    @property
    @abstractmethod
    def providers(self) -> Iterable[IConfigurationProvider]:
        """The IConfigurationProviders for this configuration."""
        pass

class IConfigurationSection(IConfiguration):
    """Represents a section of application configuration values."""
    @property
    @abstractmethod
    def key(self) -> str:
        """Gets the key this section occupies in its parent."""
        pass

    @property
    @abstractmethod
    def path(self) -> str:
        """Gets the full path to this section within the IConfiguration."""
        pass

    @property
    @abstractmethod
    def value(self) -> str:
        pass

    @value.setter
    @abstractmethod
    def value(self, value: str) -> None:
        pass

class IConfigurationSource(ABC):
    """Represents a source of configuration key/values for an application."""
    @abstractmethod
    def build(self, builder: IConfigurationBuilder) -> IConfigurationProvider:
        """Builds the IConfigurationProvider for this source.
        
        :param IConfigurationBuilder builder: The IConfigurationBuilder.
        :return: An IConfigurationProvider.
        """
        pass