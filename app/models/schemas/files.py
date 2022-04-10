from enum import Enum

from pydantic import BaseModel


class ObjectType(str, Enum):
    user_post = "user_post"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class ContentType(str, Enum):
    jpg = "image/jpeg"
    png = "image/png"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class UrlInResponse(BaseModel):
    public_url: str
