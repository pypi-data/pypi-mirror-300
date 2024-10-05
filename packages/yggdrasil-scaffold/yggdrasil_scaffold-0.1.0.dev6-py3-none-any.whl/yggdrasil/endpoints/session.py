# coding=utf-8
"""注册 Yggdrasil API 的会话端点"""
from typing import Annotated, Literal

from Crypto.PublicKey.RSA import RsaKey
from adofai import SerializedProfile
from adofai.models import FulfilledGameProfile
from fastapi import APIRouter, Depends, Response

from yggdrasil.endpoints import handlers
from yggdrasil.exceptions import InvalidToken

session_endpoints = APIRouter(prefix="/sessionserver/session/minecraft")


@session_endpoints.post("/join", status_code=204)
async def join(result: Annotated[bool, Depends(handlers.session.join)]) -> None:
    """处理玩家侧正版验证逻辑"""
    if not result:
        raise InvalidToken


@session_endpoints.get("/hasJoined")
async def has_joined(
        game_profile: Annotated[FulfilledGameProfile | Literal[False], Depends(handlers.session.has_joined)],
        sign_key: Annotated[RsaKey, Depends(handlers.root.sign_key)],
        rsp: Response) -> SerializedProfile | None:
    """处理服务侧正版验证逻辑"""
    if game_profile:
        return game_profile.serialize("full", sign_key)
    else:
        rsp.status_code = 204
        return None
