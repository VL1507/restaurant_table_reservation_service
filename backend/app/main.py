import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import uvicorn
from fastapi import FastAPI

from app.api import api_router
from app.cors import setup_cors
from app.utils.custom_logger import custom_logging_basicConfig, setup_logger

custom_logging_basicConfig(level=logging.DEBUG)

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    logger.info("app start")
    yield
    logger.info("app stop")


app = FastAPI(lifespan=lifespan)


setup_cors(app)


app.include_router(router=api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
