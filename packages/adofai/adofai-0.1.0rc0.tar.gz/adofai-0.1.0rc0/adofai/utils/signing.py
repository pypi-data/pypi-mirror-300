# coding=utf-8
"""RSA 签名工具"""
__all__ = ["dummy_key", "sign_property"]

from base64 import b64encode
from functools import lru_cache

from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15


@lru_cache(maxsize=1)
def dummy_key(length: int = 2048) -> RsaKey:
    """在不需要持久化签名密钥的场景下使用统一签名密钥的快捷方式，密钥长度至少为2048，标准推荐为4096"""
    return RSA.generate(length)


def sign_property(value: str, key: RsaKey) -> str:
    """以提供的值和 RSA 私钥对指定内容签名
    :param value: 待签名的值
    :param key: 用于签名的私钥
    :return: Base64 编码的签名结果
    """
    message = value.encode()
    h = SHA1.new(message)
    signature = b64encode(pkcs1_15.new(key).sign(h)).decode()
    return signature
