# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ConfigExecuteParams", "Message"]


class ConfigExecuteParams(TypedDict, total=False):
    session_id: Required[str]

    id: str

    api_key: str

    concurrent: bool

    messages: Iterable[Message]

    metadata: object

    run_id: str

    stream: bool


class Message(TypedDict, total=False):
    content: Required[str]

    role: Required[Literal["model", "user", "system"]]

    uuid: Annotated[str, PropertyInfo(alias="UUID")]
