# coding=utf-8
"""Yggdrasil 客户端"""
__all__ = ["AbstractProvider", "MojangProvider", "AuthInjCompatibleProvider"]

import warnings
from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import partial
from typing import Any, Literal, Optional, Self, override

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from adofai import GameId, GameName, SerializedProfile
from adofai.models import FulfilledGameProfile, GameProfile, PartialGameProfile
from adofai.utils.uuid import uuid_to_str
from aiohttp import ClientSession, DummyCookieJar

from yggdrasil_client.exceptions import FailedStatusCode, NotSupported


class AbstractProvider(ABC):
    """接口基类"""

    async def has_joined(self, username: GameName, serverId: str,
                         ip: Optional[str] = None) -> FulfilledGameProfile | Literal[False]:
        """服务端验证客户端"""
        content = await self.has_joined_raw(username=username, serverId=serverId, ip=ip)
        return content and FulfilledGameProfile(GameProfile.deserialize(content))

    async def has_joined_raw(self, username: GameName, serverId: str,
                             ip: Optional[str] = None) -> SerializedProfile | None:
        """服务端验证客户端，为保留签名，不作反序列化处理"""
        raise NotImplementedError

    async def query_by_uuid(self, uuid: GameId) -> FulfilledGameProfile | None:  # 参数名勿改
        """通过单个玩家 UUID 查询完整玩家档案"""
        content = await self.query_by_uuid_raw(uuid)
        return content and FulfilledGameProfile(GameProfile.deserialize(content))

    async def query_by_uuid_raw(self, uuid: GameId) -> SerializedProfile | None:
        """通过单个玩家 UUID 查询完整玩家档案，为保留签名，不作反序列化处理"""
        raise NotImplementedError

    async def query_by_names(self, names: list[GameName]) -> list[PartialGameProfile]:
        """通过多个玩家名查询玩家档案"""
        raise NotImplementedError

    async def query_by_name(self, name: GameName) -> PartialGameProfile | None:
        """通过单个玩家名查询玩家档案"""
        raise NotImplementedError

    async def profile_public_keys(self) -> list[RsaKey]:
        """用于验证玩家档案材质属性的公钥列表"""
        raise NotImplementedError

    async def profile_public_key(self) -> RsaKey:
        """用于验证玩家档案材质属性的公钥"""
        raise NotImplementedError


class AiohttpProvider(AbstractProvider):
    @abstractmethod
    def __init__(self, *, session_factory: Optional[Callable[[str], ClientSession]] = None):
        self._session_factory = session_factory
        self._session: ClientSession

    def _ensure_session(self) -> ClientSession:
        """只是单纯地建立会话"""
        session_factory = self._session_factory or partial(ClientSession, cookies=DummyCookieJar())
        if not hasattr(self, "_session"):
            self._session = session_factory()
        elif self._session.closed:
            self._session = session_factory()
        return self._session

    async def close(self) -> None:
        """关闭内部连接"""
        await self._session.close()

    async def __aenter__(self) -> Self:
        self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()


class MojangProvider(AiohttpProvider):
    @override
    def __init__(self, *, session_factory: Optional[Callable[[str], ClientSession]] = None):
        self._session_factory = session_factory
        self._session: ClientSession

    @override
    async def has_joined_raw(self, username: GameName, serverId: str,
                             ip: Optional[str] = None) -> SerializedProfile | None:
        full_url = "https://sessionserver.mojang.com/session/minecraft/hasJoined"
        params = {
            "username": username,
            "serverId": serverId,
        }
        if ip:
            params["ip"] = ip
        async with self._ensure_session().get(full_url, params=params) as resp:
            if resp.ok:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return None
            raise FailedStatusCode(resp.status)

    @override
    async def query_by_uuid_raw(self, uuid: GameId) -> SerializedProfile | None:
        full_url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid_to_str(uuid)}?unsigned=false"
        async with self._ensure_session().get(full_url) as resp:
            if resp.status == 200:
                return await resp.json()
            elif resp.status == 204:
                return None
            raise FailedStatusCode(resp.status)

    @override
    async def query_by_names(self, names: list[GameName]) -> list[PartialGameProfile]:
        full_url = "https://api.minecraftservices.com/minecraft/profile/lookup/bulk/byname"
        async with self._ensure_session().post(full_url, json=names) as resp:
            if resp.status == 200:
                content = await resp.json()
                return [PartialGameProfile(GameProfile.deserialize(i)) for i in content]
            raise FailedStatusCode(resp.status)

    @override
    async def query_by_name(self, name: GameName) -> PartialGameProfile | None:
        full_url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
        async with self._ensure_session().get(full_url) as resp:
            if resp.status == 200:
                content = await resp.json()
                return PartialGameProfile(GameProfile.deserialize(content))
            elif resp.status in (204, 404):
                return None
            raise FailedStatusCode(resp.status)

    @override
    async def profile_public_keys(self) -> list[RsaKey]:
        full_url = "https://api.minecraftservices.com/publickeys"
        async with self._ensure_session().get(full_url) as resp:
            if resp.status == 200:
                content = await resp.json()
                return [RSA.import_key(i["publicKey"]) for i in content["profilePropertyKeys"]]
        raise FailedStatusCode(resp.status)

    @override
    async def profile_public_key(self) -> Any:
        raise NotSupported("Mojang has multiple public keys, please use `profile_public_keys` instead")


class AuthInjCompatibleProvider(AiohttpProvider):
    @override
    def __init__(self, url: str, *, try_ali: bool = False,
                 session_factory: Optional[Callable[[str], ClientSession]] = None):
        # TODO：ALI
        self._prefix: str = url
        self._session_factory = session_factory
        self._session: ClientSession

    @override
    async def has_joined_raw(self, username: GameName, serverId: str,
                             ip: Optional[str] = None) -> FulfilledGameProfile | None:
        full_url = f"{self._prefix}/sessionserver/session/minecraft/hasJoined"
        params = {
            "username": username,
            "serverId": serverId,
        }
        if ip:
            params["ip"] = ip
        async with self._ensure_session().get(full_url, params=params) as resp:
            if resp.ok:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status == 204:
                    return None
            raise FailedStatusCode(resp.status)

    @override
    async def query_by_uuid_raw(self, uuid: GameId) -> SerializedProfile | None:
        full_url = f"{self._prefix}/sessionserver/session/minecraft/profile/{uuid_to_str(uuid)}?unsigned=false"
        async with self._ensure_session().get(full_url) as resp:
            if resp.status == 200:
                return await resp.json()
            elif resp.status == 204:
                return None
        raise FailedStatusCode(resp.status)

    @override
    async def query_by_names(self, names: list[GameName]) -> list[PartialGameProfile]:
        full_url = f"{self._prefix}/api/profiles/minecraft"
        async with self._ensure_session().post(full_url, json=names) as resp:
            if resp.status == 200:
                content = await resp.json()
                return [PartialGameProfile(GameProfile.deserialize(i)) for i in content]
            raise FailedStatusCode(resp.status)

    @override
    async def query_by_name(self, name: GameName) -> PartialGameProfile | None:
        result = await self.query_by_names([name])
        return result[0] if result else None

    @override
    async def profile_public_keys(self) -> list[RsaKey]:
        warnings.warn(
            "Mojang has multiple profile public keys, " +
            "but Authlib-injector compatible providers don't. " +
            "Therefore this method isn't necessary and may be removed one day.",
            FutureWarning,
            stacklevel=2
        )
        result = await self.profile_public_key()
        return [result]

    @override
    async def profile_public_key(self) -> RsaKey:
        full_url = f"{self._prefix}/"
        async with self._ensure_session().get(full_url) as resp:
            if resp.status == 200:
                content = await resp.json()
                if key_str := content.get("signaturePublickey"):
                    return RSA.import_key(key_str)
                else:
                    raise NotSupported
            raise FailedStatusCode(resp.status)


if __name__ == "__main__":
    import asyncio
    from uuid import UUID


    async def usage_example():
        littleskin = AuthInjCompatibleProvider("https://littleskin.cn/api/yggdrasil")
        mojang = MojangProvider()
        async with littleskin as r:
            print(await r.has_joined(GameName("Notch"), "serverid"))
            print(await r.query_by_name(GameName("NoTcH")))
            print((await r.profile_public_key()).export_key().decode())
            print((await r.profile_public_keys())[0].export_key().decode())

        async with mojang as r:
            print(await r.has_joined(GameName("Notch"), "serverid"))
            print(await r.query_by_name(GameName("Notch")))

            print(await r.query_by_uuid(GameId(UUID("069a79f444e94726a5befca90e38aaf5"))))
            print(await r.query_by_uuid_raw(GameId(UUID("069a79f444e94726a5befca90e38aaf5"))))


    asyncio.run(usage_example())
