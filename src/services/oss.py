from sanic import HTTPResponse

from src.utils.oss import OSS, AsyncObjectAdapter
from src.utils.result import Result
from src.utils.stream import sanic_async_stream


async def sanic_send_oss_file(
    oss: OSS,
    path: str,
) -> HTTPResponse:
    headers = {}
    try:
        f = await oss.get_object(path)
    except:
        return Result.not_found()
    content_length = f.content_length
    headers.update(
        {
            "Content-Length": content_length,
            "x-oss-hash-crc64ecma": f.server_crc,
        }
    )
    filename = path.split("/")[-1]
    adapter = AsyncObjectAdapter(f)
    mime_type = f.content_type
    result = await sanic_async_stream(
        adapter,
        filename=filename,
        mime_type=mime_type,
        headers=headers,
    )
    return result  # type: ignore
