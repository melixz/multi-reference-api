from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.schemas.common import ErrorResponse


app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(api_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else "Request error"
    errors = None
    if not isinstance(exc.detail, str):
        errors = {"detail": [jsonable_encoder(exc.detail)]}

    payload = ErrorResponse(
        message=message,
        errors=errors,
        error_code="HTTP_ERROR",
    ).model_dump()
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors: dict[str, list[str]] = {}
    for err in exc.errors():
        location = ".".join(str(part) for part in err["loc"] if part != "body")
        errors.setdefault(location, []).append(err["msg"])

    payload = ErrorResponse(
        message="Validation failed",
        errors=errors,
        error_code="VALIDATION_ERROR",
    ).model_dump()
    return JSONResponse(status_code=422, content=payload)
