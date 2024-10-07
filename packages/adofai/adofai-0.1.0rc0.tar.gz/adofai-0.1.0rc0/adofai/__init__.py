# coding=utf-8
"""定义类型别名"""
__all__ = ["AccessToken", "ClientToken", "UserId", "UserLoginName", "GameId", "GameName", "TextureUrl",
           "VersionNumber", "ProfileProperties", "SerializedProfile"]

from typing import Mapping, NewType
from uuid import UUID

AccessToken = NewType('AccessToken', str)
ClientToken = NewType('ClientToken', str)
UserId = NewType('UserId', UUID)
UserLoginName = NewType('UserLoginName', str)
GameId = NewType('GameId', UUID)
GameName = NewType('GameName', str)
TextureUrl = NewType('TextureUrl', str)
VersionNumber = NewType('VersionNumber', str)

type ProfileProperties = Mapping[str, str]
type SerializedProfile = dict[str, list[dict[str, str]] | str]
