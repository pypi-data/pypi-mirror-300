from pydantic import BaseModel


class PositionResponseDto(BaseModel):
    code: str | None
    comment: str | None
    id: str | None
    is_removed: bool | None
    name: str | None

# class LEmployeePositionsData