from pydantic import BaseModel


class machine(BaseModel):
    id: int
    status: dict[str, bool]
