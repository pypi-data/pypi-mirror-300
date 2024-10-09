from requests import Response

__all__ = ["dump_all"]

def dump_all(response: Response, request_prefix: bytes = b"< ", response_prefix: bytes = b"> ") -> bytearray: ...
