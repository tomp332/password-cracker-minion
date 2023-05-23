from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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
    pass

# include routes
