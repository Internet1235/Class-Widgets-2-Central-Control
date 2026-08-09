from fastapi import FastAPI

from .routers import admin, auth, device

app = FastAPI(
    title="Class Widgets Central Control",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/docs",
)
app.include_router(admin.router, prefix="/api/v1/admin")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(device.router, prefix="/api/v1/device")


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
