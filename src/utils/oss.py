import asyncio
import os
from abc import ABC, abstractmethod

import oss2
from dotenv import load_dotenv
from oss2.api import GetObjectResult


class BaseAsyncReaderableBufferAdapter(ABC):
    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    async def __anext__(self) -> bytes:
        ...

    def __aiter__(self):
        return self


class AsyncObjectAdapter(BaseAsyncReaderableBufferAdapter):
    def __init__(self, file: GetObjectResult, buffer_size: int = 4096) -> None:
        self._file = file
        self._buffer_size = buffer_size

    async def __anext__(self) -> bytes:
        data: bytes = await asyncio.to_thread(
            self._file.read,  # type: ignore
            self._buffer_size,
        )
        if not data:
            raise StopAsyncIteration
        return data


class OSS:
    def __init__(
        self,
        oss_access_key_id: str,
        oss_access_key_secret: str,
        oss_endpoint: str,
        bucket_name: str,
    ):
        self._access_key_id = oss_access_key_id
        self._access_key_secret = oss_access_key_secret
        self._auth = oss2.Auth(
            self._access_key_id,
            self._access_key_secret,
        )
        self._service = oss2.Service(self._auth, oss_endpoint)
        self._bucket = oss2.Bucket(
            self._auth,
            oss_endpoint,
            bucket_name,
        )

    @staticmethod
    def from_env() -> "OSS":
        load_dotenv()
        oss_access_key_id = os.getenv("OSS_ACCESS_KEY_ID") or ""
        oss_access_key_secret = os.getenv("OSS_ACCESS_KEY_SECRET") or ""
        oss_endpoint = os.getenv("OSS_ENDPOINT") or ""
        bucket_name = os.getenv("OSS_BUCKET_NAME") or ""
        return OSS(
            oss_access_key_id=oss_access_key_id,
            oss_access_key_secret=oss_access_key_secret,
            oss_endpoint=oss_endpoint,
            bucket_name=bucket_name,
        )

    async def get_object(self, path: str):
        return await asyncio.to_thread(self._bucket.get_object, path)


async def test():
    oss = OSS.from_env()
    f = await oss.get_object("test.txt")
    k = 0
    async for i in AsyncObjectAdapter(f):
        print(f"it: {k:5} {len(i)} | {i[:20]}")
        k += 1

    print(f.client_crc, f.server_crc)


if __name__ == "__main__":
    asyncio.run(test())
