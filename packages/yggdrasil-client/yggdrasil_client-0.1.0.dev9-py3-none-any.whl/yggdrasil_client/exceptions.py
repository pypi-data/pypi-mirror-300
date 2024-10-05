# coding=utf-8
"""定义异常"""
__all__ = ["YggdrasilClientException", "ProviderException", "FailedStatusCode", "NotSupported"]

from typing import Optional


class YggdrasilClientException(Exception):
    """Yggdrasil Client 根异常"""


class ProviderException(YggdrasilClientException):
    """服务提供方问题"""


class FailedStatusCode(ProviderException):
    """状态码不在标准定义中"""

    def __init__(self, status_code: Optional[int] = None):
        self.add_note(f"Status Code: {status_code}")


class NotSupported(ProviderException):
    """自定义 Yggdrasil 服务器似乎没有实现，或是不支持相关功能。注意不是 501 状态码"""

    def __init__(self, detail: Optional[str] = None):
        if detail:
            self.add_note(detail)
