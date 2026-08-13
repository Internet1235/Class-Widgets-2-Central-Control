import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routers import admin, auth, automation, device
from .services.automation import worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    stop_event = asyncio.Event()
    task = asyncio.create_task(worker(stop_event))
    app.state.automation_stop = stop_event
    try:
        yield
    finally:
        stop_event.set()
        await task

app = FastAPI(
    title="Class Widgets Central Control",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/docs",
    lifespan=lifespan,
)
app.include_router(admin.router, prefix="/api/v1/admin")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(device.router, prefix="/api/v1/device")
app.include_router(automation.router, prefix="/api/v1/admin/automations")


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
