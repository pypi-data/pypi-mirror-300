# Yggdrasil Client based on ADOFAI

基于 [ADOFAI](https://github.com/silverteal/adofai) 和 aiohttp 的 Minecraft Yggdrasil 协议兼容客户端，支持
Mojang 后端。

目前已经实现了 Authlib-Injector Yggdrasil 协议中所有公共（无需认证） API 的包装

Yggdrasil 是 Minecraft 中身份验证服务的实现名称。

## 快速开始

### 安装

```shell
pip install yggdrasil-client
```

### 示例

```python
import asyncio
from uuid import UUID
from adofai import GameName, GameId
from yggdrasil_client import AuthInjCompatibleProvider, MojangProvider


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


if __name__ == "__main__":
    asyncio.run(usage_example())

```

## 另请参阅

[ADOFAI](https://github.com/silverteal/adofai) 是一组数据模型和配套工具，旨在简化自定义实现 Authlib-injector 的规范
Yggdrasil 服务端、客户端及其配套程序的过程。

[Yggdrasil Scaffold](https://github.com/silverteal/yggdrasil-scaffold) 是基于 ADOFAI 和 FastAPI 的 Yggdrasil
身份验证协议实现脚手架。