import struct

from enum import Enum
from pydantic import BaseModel, Field
from typing import ClassVar


class RequestType(Enum):
    ECHO = 0
    AUTHENTICATE = 1
    GET_MESSAGES = 2
    LIST_USERS = 3
    SEND_MESSAGE = 4
    READ_MESSAGES = 5
    DELETE_MESSAGES = 6
    DELETE_USER = 7


class ResponseType(Enum):
    ECHO = 0
    AUTHENTICATE = 1
    GET_MESSAGES = 2
    LIST_USERS = 3
    SEND_MESSAGE = 4
    READ_MESSAGES = 5
    DELETE_MESSAGES = 6
    DELETE_USER = 7
    ERROR = 8


class DataType(Enum):
    NULL = 0
    MESSAGE = 1
    LIST = 2


class Header(BaseModel):
    """
    Header object class: the fundamental building block of the wire protocol.
    """

    FORMAT: ClassVar[str] = "!B I"
    SIZE: ClassVar[int] = struct.calcsize(FORMAT)

    header_type: int
    payload_size: int = Field(default=0)

    def pack(self) -> bytes:
        """
        Serialization format:
            <HEADER_TYPE> <PAYLOAD_SIZE>
        """
        return struct.pack(self.FORMAT, self.header_type, self.payload_size)

    @staticmethod
    def unpack(data: bytes) -> "Header":
        header_type, payload_size = struct.unpack_from(Header.FORMAT, data)
        return Header(header_type=header_type,
                      payload_size=payload_size)
