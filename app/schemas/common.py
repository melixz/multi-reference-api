from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    success: bool = True
    data: T


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: dict[str, list[str]] | None = None
    error_code: str | None = None
