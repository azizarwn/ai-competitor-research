from fastapi import FastAPI
from app.modules.research.task import research_task
from app.modules.research.schema import ResearchInput
from scalar_fastapi import get_scalar_api_reference
from app.core.settings import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url=None,
    redoc_url=None,
)


@app.post("/research")
def do_research(body: ResearchInput):
    research_task.delay(body.product_description)
    return {"message": "Processing..."}


@app.get("/")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
