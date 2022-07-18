from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import cfg
from api.v1 import films, persons, genres
from db import storage


app = FastAPI(
    title=cfg.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    storage.adapter = storage.ElasticStorage(cfg)


@app.on_event('shutdown')
async def shutdown():
    await storage.adapter.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
