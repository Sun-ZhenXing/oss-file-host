from dataclasses import dataclass
from typing import Any

from sanic import json


@dataclass
class Result:
    code: int = 0
    msg: str = ""
    data: Any = None
    http_code: int = 200

    def to_json(self, **kwargs):
        return json(
            {
                "code": self.code,
                "msg": self.msg,
                "data": self.data,
            },
            status=self.http_code,
            **kwargs,
        )

    @staticmethod
    def success(data: Any = None):
        return Result(data=data).to_json()

    @staticmethod
    def fail(
        msg: str = "",
        code: int = -1,
        data: Any = None,
        http_code: int = 200,
    ):
        return Result(
            code=code,
            msg=msg,
            data=data,
            http_code=http_code,
        ).to_json()

    @staticmethod
    def not_found(msg: str = "Not Found", http_code: int = 200):
        return Result(
            code=-1,
            msg=msg,
            http_code=http_code,
        ).to_json()
