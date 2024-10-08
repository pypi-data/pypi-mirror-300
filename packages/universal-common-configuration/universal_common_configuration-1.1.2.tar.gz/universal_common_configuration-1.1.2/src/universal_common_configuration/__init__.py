# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.

from __future__ import annotations

from collections.abc import Iterable
from functools import cmp_to_key
from typing import Callable, Optional

from .abstractions import ConfigurationPath, IComparer, IConfiguration, IConfigurationBuilder, IConfigurationProvider, IConfigurationRoot, IConfigurationSection, IConfigurationSource

class ConfigurationKeyComparer(IComparer):
    """IComparer implementation used to order configuration keys."""
    KEY_DELIMITER: str = ":"
    instance: ConfigurationKeyComparer
    comparison: Callable[[Optional[str], Optional[str]], int]

    def compare(self, x: Optional[str], y: Optional[str]) -> int:
        def skip_ahead_on_delimiter(a: str):
            while a and a[0] == ConfigurationKeyComparer.KEY_DELIMITER:
                a = a[1:]
            return a
        
        def compare(a: str, b:str):
            def try_parse(str: str) -> tuple[bool, Optional[int]]:
                value: Optional[int] = None
                try:
                    value = int(str)
                    return True, value
                except:
                    return False, None

            a_is_int, value1 = try_parse(a)
            b_is_int, value2 = try_parse(b)

            result: int

            if not a_is_int and not b_is_int:
                transformed_a = a.casefold()
                transformed_b = b.casefold()

                if transformed_a == transformed_b:
                    result = 0
                else:
                    result = -1 if transformed_a < transformed_b else 1
            elif a_is_int and b_is_int:
                result = value1 - value2
            else:
                result = -1 if a_is_int else 1

            return result
        
        x_span: Optional[str] = x
        y_span: Optional[str] = y

        x_span = skip_ahead_on_delimiter(x_span)
        y_span = skip_ahead_on_delimiter(y_span)

        while x_span and y_span:
            x_delimiter_index: int = -1
            if ConfigurationKeyComparer.KEY_DELIMITER in x_span:
                x_delimiter_index = x_span.index(ConfigurationKeyComparer.KEY_DELIMITER)
            y_delimiter_index: int = -1
            if ConfigurationKeyComparer.KEY_DELIMITER in y_span:
                y_delimiter_index = y_span.index(ConfigurationKeyComparer.KEY_DELIMITER)

            compare_result: int = compare(x_span if x_delimiter_index == -1 else x_span[:x_delimiter_index], y_span if y_delimiter_index == -1 else y_span[:y_delimiter_index])

            if compare_result != 0:
                return compare_result
            
            x_span = None if x_delimiter_index == -1 else skip_ahead_on_delimiter(x_span[x_delimiter_index + 1:])
            y_span = None if y_delimiter_index == -1 else skip_ahead_on_delimiter(y_span[y_delimiter_index + 1:])

        return (0 if not y_span else -1) if not x_span else 1
    
ConfigurationKeyComparer.instance = ConfigurationKeyComparer()
ConfigurationKeyComparer.comparison = ConfigurationKeyComparer.instance.compare

class ConfigurationBuilder(IConfigurationBuilder):
    """Used to build key/value based configuration settings for use in an application."""
    _properties: dict[str, object]
    _sources: list[IConfigurationSource]

    def __init__(self):
        self._properties = dict()
        self._sources = list()

    @property
    def sources(self) -> list[IConfigurationSource]:
        """Returns the sources used to obtain configuration values."""
        return self._sources

    @property
    def properties(self) -> dict[str, object]:
        """Gets a key/value collection that can be used to share data between the ConfigurationBuilder and the registered ConfigurationProviders."""
        return self._properties

    def add(self, source: IConfigurationSource) -> IConfigurationBuilder:
        """Adds a new configuration source.
        
        :param IConfigurationSource source: The configuration source to add.
        :return: The same ConfigurationBuilder.
        """
        if source is None:
            raise ValueError("source cannot be None.")
        
        self._sources.append(source)

        return self
    
    def build(self) -> IConfigurationRoot:
        providers: list[IConfigurationProvider] = list()
        for source in self._sources:
            provider = source.build(self)
            providers.append(provider)

        return ConfigurationRoot(providers)

class ConfigurationProvider(IConfigurationProvider):
    """Base helper class for implementing an IConfigurationProvider"""
    data: dict[str, Optional[str]]

    def __init__(self):
        self.data = dict()

    def try_get(self, key: str) -> tuple[bool, Optional[str]]:
        """Attempts to find a value with the given key, returns True if one is found, False otherwise."""
        transformed_key: str = key.casefold()
        matching_key: Optional[str] = next((key for key in self.data.keys() if key.casefold() == transformed_key), None)
        if matching_key:
            return True, self.data[matching_key]
        else:
            return False, None
        
    def set(self, key: str, value: Optional[str]) -> None:
        """Sets a value for a given key.
        
        :param str key: The configuration key to set.
        :param Optional[str] value: The value to set."""
        self.data[key] = value

    def load() -> None:
        pass

    def get_child_keys(self, earlier_keys: Iterable[str], parent_path: Optional[str]) -> Iterable[str]:
        results: list[str] = list()

        if parent_path is None:
            key: str
            for key in self.data.keys():
                results.append(ConfigurationProvider.segment(key, 0))
        else:
            key: str
            for key in self.data.keys():
                if (len(key) > len(parent_path) and 
                    key.casefold().startswith(parent_path.casefold()) and 
                    key[len(parent_path)] == ConfigurationPath.KEY_DELIMITER):
                    results.append(ConfigurationProvider.segment(key, len(parent_path) + 1))

        results.extend(earlier_keys)
        results = sorted(results, key=cmp_to_key(ConfigurationKeyComparer.comparison))

        return results
    
    @staticmethod
    def segment(key: str, prefix_length: int):
        try:
            index_of: int = key.index(ConfigurationPath.KEY_DELIMITER, prefix_length)
            return key[prefix_length:index_of]
        except ValueError:
            return key[prefix_length]
    
class ConfigurationRoot(IConfigurationRoot):
    """The root node for a configuration."""
    _providers: list[IConfigurationProvider]
    
    def __init__(self, providers: list[IConfigurationProvider]):
        """Initializes a Configuration root with a list of providers."""
        if providers is None:
            raise ValueError("providers cannot be None.")

        self._providers = providers
        provider: IConfigurationProvider
        for provider in providers:
            provider.load()

    @property
    def providers(self) -> Iterable[IConfigurationProvider]:
        """The IConfigurationProviders for this configuration."""
        return self._providers
    
    def __getitem__(self, key: str) -> Optional[str]:
        """Gets the value corresponding to a configuration key."""
        return self.get_configuration(self._providers, key)
    
    def __setitem__(self, key: str, value: Optional[str]) -> None:
        """Sets the value corresponding to a configuration key."""
        self.set_configuration(self._providers, key, value)

    def get_children(self) -> Iterable[IConfigurationSection]:
        """Gets the immediate children sub-sections."""
        return self.get_children_implementation(None)
    
    def get_section(self, key: str) -> IConfigurationSection:
        """Gets a configuration sub-section with the specified key.
        
        :param str key: The key of the configuration section.
        :returns: The IConfigurationSection.
        :rtype: IConfigurationSection"""
        return ConfigurationSection(self, key)
    
    def reload(self) -> None:
        """Force the configuration values to be reloaded from the underlying sources."""
        provider: IConfigurationProvider
        for provider in self._providers:
            provider.load()

    @staticmethod
    def get_configuration(providers: list[IConfigurationProvider], key: str) -> Optional[str]:
        i: int
        for i in range(len(providers) - 1, -1, -1):
            provider: IConfigurationProvider = providers[i]

            condition: bool
            value: Optional[str]
            condition, value = provider.try_get(key)
            if (condition):
                return value

        return None
    
    @staticmethod
    def set_configuration(providers: list[IConfigurationProvider], key: str, value: Optional[str]) -> None:
        if len(providers) == 0:
            raise ValueError("No configuration sources were configured.")
        
        provider: IConfigurationProvider
        for provider in providers:
            provider.set(key, value)

    def get_children_implementation(root: IConfigurationRoot, path: Optional[str]) -> Iterable[IConfigurationSection]:
        """Gets the immediate children sub-sections of configuration root based on key."""
        providers: Iterable[IConfigurationProvider] = root.providers

        child_keys: list[str] = list()
        provider: IConfigurationProvider
        for provider in providers:
            child_keys.extend(provider.get_child_keys(child_keys, path))
        unique_child_keys = list()
        child_key: str
        for child_key in child_keys:
            transformed_child_key = child_key.casefold()
            if not any(unique_key.casefold() == transformed_child_key for unique_key in unique_child_keys):
                unique_child_keys.append(child_key)

        children: list[IConfigurationSection] = list()
        key: str
        for key in unique_child_keys:
            children.append(root.get_section(key if not path else path + ConfigurationPath.KEY_DELIMITER + key))

        return children
    
class ConfigurationSection(IConfigurationSection):
    """Represents a section of application configuration values."""
    _root: IConfigurationRoot
    _path: str
    _key: Optional[str]

    def __init__(self, root: IConfigurationRoot, path: str):
        self._root = root
        self._path = path
        self._key = None

    @property
    def path(self) -> str:
        """Gets the full path to this section from the IConfigurationRoot."""
        return self._path
    
    @property
    def key(self) -> str:
        """Gets the key this section occupies in its parent."""
        # Key is calculated lazily as last portion of Path
        if self._key is None:
            self._key = ConfigurationPath.get_section_key(self._path)

        return self._key
    
    @property
    def value(self) -> str:
        """Gets the section value."""
        return self._root[self.path]
    
    @value.setter
    def value(self, value: str) -> None:
        """Sets the section value."""
        self._root[self.path] = value

    def __getitem__(self, key: str) -> Optional[str]:
        return self._root[self.path + ConfigurationPath.KEY_DELIMITER + key]
    
    def __setitem__(self, key: str, value: Optional[str]) -> None:
        self._root[self.path + ConfigurationPath.KEY_DELIMITER + key] = value

    def get_section(self, key: str) -> IConfigurationSection:
        """Gets a configuration sub-section with the specified key.
        
        :param str key: The key of the configuration section.
        :returns: The IConfigurationSection.
        :rtype: IConfigurationSection"""
        return self._root.get_section(self.path + ConfigurationPath.KEY_DELIMITER + key)
    
    def get_children(self) -> Iterable[IConfigurationSection]:
        """Gets the immediate descendant configuration sub-sections."""
        return self._root.get_children_implementation(self.path)