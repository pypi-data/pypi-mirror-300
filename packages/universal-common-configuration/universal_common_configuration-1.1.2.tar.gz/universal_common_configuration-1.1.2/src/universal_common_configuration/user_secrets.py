# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import userpaths

from . import ConfigurationProvider
from .abstractions import IConfigurationBuilder, IConfigurationProvider, IConfigurationSource
from .json import JsonConfigurationParser

class PathHelper:
    SECRETS_FILE_NAME: str = "secrets.json"

    @staticmethod
    def get_secrets_path_from_secrets_id(user_secrets_id: str) -> str:
        return PathHelper.internal_get_secrets_path_from_secrets_id(user_secrets_id, True)
    
    @staticmethod
    def internal_get_secrets_path_from_secrets_id(user_secrets_id: str, throw_if_no_root: bool):
        if not user_secrets_id:
            raise ValueError("user_secrets_id must be provided.")
        
        USER_SECRETS_FALLBACK_DIR: str = "DOTNET_USER_SECRETS_FALLBACK_DIR"

        app_data: Optional[str] = os.environ.get("APPDATA")
        root: Optional[str] = app_data
        root = root if root else os.environ.get("HOME")
        root = root if root else userpaths.get_appdata()
        root = root if root else userpaths.get_profile()
        root = root if root else os.environ.get(USER_SECRETS_FALLBACK_DIR)

        if not root:
            if throw_if_no_root:
                raise ValueError("Cannot determine valid user secrets location.")
            
            return ""
        
        return os.path.join(root, "Microsoft", "UserSecrets", user_secrets_id, PathHelper.SECRETS_FILE_NAME) if app_data else os.path.join(root, ".microsoft", "usersecrets", user_secrets_id, PathHelper.SECRETS_FILE_NAME)

class UserSecretsConfigurationProvider(ConfigurationProvider):
    def __init__(self, user_secrets_id: str):
        self.user_secrets_id = user_secrets_id

    def load(self) -> None:
        secrets_path = PathHelper.get_secrets_path_from_secrets_id(self.user_secrets_id)
        path: Path = Path(secrets_path)
        self.data = JsonConfigurationParser.parse_file(path)

class UserSecretsConfigurationSource(IConfigurationSource):
    def __init__(self, user_secrets_id: str):
        self.user_secrets_id = user_secrets_id

    def build(self, builder: IConfigurationBuilder) -> IConfigurationProvider:
        return UserSecretsConfigurationProvider(self.user_secrets_id)

def _add_user_secrets(self, user_secrets_id: str) -> IConfigurationBuilder:
    self.add(UserSecretsConfigurationSource(user_secrets_id))
    return self

IConfigurationBuilder.add_user_secrets = _add_user_secrets