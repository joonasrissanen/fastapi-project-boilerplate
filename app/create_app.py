from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import router
from app.db.database import sessionmanager
from app.exceptions import NotFoundError
from app.logger import configure_logging, logger
from app.settings import settings


def init_lifespan():
    sessionmanager.init(settings.database_url)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        yield
        if sessionmanager._engine is not None:  # pyright: ignore[reportPrivateUsage]
            await sessionmanager.close()

    return lifespan


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_exception_handler(  # pyright: ignore[reportUnusedFunction]
        _: Request,
        exc: NotFoundError,
    ) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(Exception)
    async def global_exception_handler(  # pyright: ignore[reportUnusedFunction]
        _: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.error("Unhandled exception", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error. Please try again later."},
        )


def create_app():
    configure_logging(
        settings.log_level, use_json=settings.environment != "development"
    )
    app = FastAPI(
        title="FastAPI Server",
        lifespan=init_lifespan(),
    )
    register_exception_handlers(app)
    logger.info("Yoyo Starting application", extra={"asd": 123})
    app.include_router(router)

    return app
