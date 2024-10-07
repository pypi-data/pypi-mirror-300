# coding=utf-8
"""档案 CRUD 相关工具"""
__all__ = ["offline_game_profile",
           "prompt_game_profile",
           "random_game_profile", "random_user_profile", "random_texture",
           "fake_token", "parse_fake_token"]

import json
from base64 import b64decode, b64encode
from random import choice, randint
from uuid import uuid4

from adofai import AccessToken, GameId, GameName, TextureUrl, UserId
from adofai.models import FulfilledGameProfile, GameProfile, PartialGameProfile, TextureProfile, TextureProperty, \
    UserProfile
from adofai.utils.uuid import offline_uuid


# 可能是这个模块里唯一一个正经函数
def offline_game_profile(name: GameName) -> PartialGameProfile:
    """根据玩家名快速生成离线玩家档案"""
    return PartialGameProfile(GameProfile(id=offline_uuid(name), name=name))


# fake game profile
def prompt_game_profile(info: str) -> PartialGameProfile:
    """生成用于文本提示的伪玩家档案，应用场景较少，但不是没有"""
    return PartialGameProfile(GameProfile(GameId(uuid4()), GameName(info)))


def random_game_profile() -> FulfilledGameProfile:
    """用于测试用途的随机玩家档案"""
    return FulfilledGameProfile(GameProfile(
        id=offline_uuid(a := GameName("player" + str(randint(1000, 9999)))),
        name=a,
        texture=random_texture(),
        extra_properties={"uploadableTextures": choice(("skin", "cape", "skin,cape"))}
    ))


# fake texture profile
def random_texture() -> TextureProfile:
    """用于测试用途的随机材质档案"""
    return TextureProfile(SKIN=TextureProperty(TextureUrl("https://hostname/sha1"),
                                               {"model": choice(("default", "slim"))}),
                          CAPE=TextureProperty(TextureUrl("https://hostname/sha1")))


# fake game profile
def random_user_profile() -> UserProfile:
    """用于测试用途的随机用户档案"""
    return UserProfile(
        id=UserId(uuid4()),
        properties={
            "preferredLanguage": choice(("en", "zh-CN", "en-CN", "en-GB", "en-US"))
        }
    )


# fake auth key
def fake_token(profile: GameProfile) -> AccessToken:
    """在安全性不敏感的场景，将游戏档案直接序列化为 AccessToken"""
    return AccessToken(b64encode(json.dumps(profile.serialize("unsigned")).encode()).decode())


def parse_fake_token(token: AccessToken) -> GameProfile:
    """在安全性不敏感的场景，解析游戏档案直接序列化的 AccessToken"""
    return GameProfile.deserialize(json.loads(b64decode(token)))
