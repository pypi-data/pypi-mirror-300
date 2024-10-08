# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.

from __future__ import annotations

import json
import os
from typing import Optional

from . import ConfigurationProvider
from .abstractions import ConfigurationPath, IConfigurationBuilder, IConfigurationProvider, IConfigurationSource

class JsonConfigurationParser:
    _data: dict[str, Optional[str]]
    _paths: list[str]

    def __init__(self):
        self._data = dict()
        self._paths = list()

    @staticmethod
    def parse_file(path: str) -> dict[str, Optional[str]]:
        if os.path.isfile(path):
            with open(path, encoding="utf-8-sig") as file:
                try:
                    return JsonConfigurationParser().parse(json.load(file))
                except:
                    return dict()

        return dict()

    @staticmethod
    def parse_string(json_string: str) -> dict[str, Optional[str]]:
        return JsonConfigurationParser().parse(json.loads(json_string))

    def parse(self, input: dict[str, any]) -> dict[str, Optional[str]]:
        self.visit_object_element(input)
        return self._data
    
    def visit_object_element(self, element: dict[str, any]) -> None:
        is_empty: bool = True

        for key, value in element.items():
            is_empty = False
            self.enter_context(key)
            self.visit_value(value)
            self.exit_context()
    
        self.set_null_if_element_is_empty(is_empty)

    def visit_array_element(self, element: any) -> None:
        index: int = 0

        for array_element in element:
            self.enter_context(str(index))
            self.visit_value(array_element)
            self.exit_context()
            index += 1

        self.set_null_if_element_is_empty(index == 0)

    def set_null_if_element_is_empty(self, is_empty: bool) -> None:
        if (is_empty and len(self._paths) > 0):
            self._data[self._paths[-1]] = None

    def visit_value(self, value: any) -> None:
        if isinstance(value, dict):
            self.visit_object_element(value)
        elif isinstance(value, list):
            self.visit_array_element(value)
        else:
            key: str = self._paths[-1]
            if next((other_key for other_key in self._data.keys() if other_key.casefold() == key.casefold()), None) is not None:
                raise ValueError("Key is duplicated.")
            self._data[key] = str(value)
    
    def enter_context(self, context: str) -> None:
        self._paths.append(self._paths[-1] + ConfigurationPath.KEY_DELIMITER + context if len(self._paths) > 0 else context)

    def exit_context(self) -> None:
        self._paths.pop()

class JsonFileConfigurationSource(IConfigurationSource):
    def __init__(self, path: str, optional: bool = True):
        self.path = path
        self.optional = optional

    def build(self, builder: IConfigurationBuilder) -> IConfigurationProvider:
        return JsonFileConfigurationProvider(self.path, self.optional)

class JsonFileConfigurationProvider(ConfigurationProvider):
    def __init__(self, path: str, optional: bool):
        super().__init__()
        self.path = path
        self.optional = optional

    def load(self) -> None:
        if not os.path.exists(self.path):
            if not self.optional:
                raise FileNotFoundError(f"The configuration file '{self.path}' was not found and is not optional.")
            self.data = {}
        else:
            self.data = JsonConfigurationParser.parse_file(self.path)

class JsonStringConfigurationProvider(ConfigurationProvider):
    def __init__(self, json_string: str):
        super().__init__()
        self.json_string = json_string

    def load(self) -> None:
        self.data = JsonConfigurationParser.parse_string(self.json_string)

class JsonStringConfigurationSource(IConfigurationSource):
    def __init__(self, json_string: str):
        self.json_string = json_string

    def build(self, builder: IConfigurationBuilder) -> IConfigurationProvider:
        return JsonStringConfigurationProvider(self.json_string)

def _add_json_file(self, file_path: str, optional: bool = True) -> IConfigurationBuilder:
    self.add(JsonFileConfigurationSource(file_path, optional))
    return self

def _add_json_string(self, json_string: str) -> IConfigurationBuilder:
    self.add(JsonStringConfigurationSource(json_string))
    return self

IConfigurationBuilder.add_json_file = _add_json_file
IConfigurationBuilder.add_json_string = _add_json_string 