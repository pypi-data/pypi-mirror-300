from pydantic import BaseModel


class ResponseModel(BaseModel):
    version: str
