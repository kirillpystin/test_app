from pydantic import BaseModel


class ObjectBody(BaseModel):
    expires: int | None = None
    data: dict
