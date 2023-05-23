from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from uvicorn.main import logger

from password_cracker_minion import minion_context
from password_cracker_minion.src.routes.main_router.router import api_router
from password_cracker_minion.src.routes.tasks_router.router import tasks_router
from password_cracker_minion.utils import minion_startup_tasks

main_api_router = FastAPI(
    title="Password Cracker Minion API",
    description="Password Cracker Minion API",
    version="1.0.0"
)

origins = ["*"]

main_api_router.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@main_api_router.on_event("startup")
async def on_startup() -> None:
    logger.info(f"Started minion server {minion_context.main_settings.minion_hostname}")
    minion_startup_tasks()


# include routes
main_api_router.include_router(tasks_router, tags=["Tasks"])
main_api_router.include_router(api_router, tags=["Main Actions"])
