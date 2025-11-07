from fastapi import FastAPI
from .database import engine, Base
from .routes import include_routers

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dota 2 API",
    description="API для управління базою даних Dota 2",
    version="1.0.0"
)

include_routers(app)


@app.get("/")
async def read_root():
    return {
        "title": "Dota 2 API",
        "description": "Ласкаво просимо до API бази даних Dota 2",
        "version": "1.0.0",
        "documentation": "/docs"
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)