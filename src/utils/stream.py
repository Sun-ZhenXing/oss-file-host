from dataclasses import dataclass
from mimetypes import guess_type
from typing import AsyncGenerator, AsyncIterable, Dict, Optional, Union

from sanic.response import ResponseStream


@dataclass
class Range:
    start: int
    end: int
    total: int


async def sanic_async_stream(
    async_iterable: Union[AsyncGenerator, AsyncIterable],
    filename: str,
    status: int = 200,
    mime_type: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    range_: Optional[Range] = None,
) -> ResponseStream:
    headers = headers or {}
    headers.setdefault(
        "Content-Disposition",
        f'attachment; filename="{filename}"',
    )
    mime_type = mime_type or guess_type(filename)[0] or "text/plain"
    if range_:
        start = range_.start
        end = range_.end
        total = range_.total
        headers["Content-Range"] = f"bytes {start}-{end}/{total}"
        status = 206

    async def _streaming_fn(response: ResponseStream):
        async for chunk in async_iterable:
            await response.write(chunk)

    return ResponseStream(
        streaming_fn=_streaming_fn,  # type: ignore
        status=status,
        headers=headers,
        content_type=mime_type,
    )
