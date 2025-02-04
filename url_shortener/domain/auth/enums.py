from enum import Enum


class JwtTokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
