from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, JsonValue
from starlette.staticfiles import StaticFiles

from product_analyzer.components.query_model import QueryModel
from product_analyzer.functions.query_pipeline import get_query_pipeline_from_model

app_router = APIRouter()

# Public folder
app_router.mount("/public", StaticFiles(directory=f"{Path.cwd()}/app/public"), name="static")

class Input(BaseModel):
    q: str
    filter: JsonValue

class Output(BaseModel):
    output: str


@app_router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app_router.post("/query")
async def get_answers(body: Input):
    query_text = body.q
    if query_text == "" or query_text is None:
        return "Please enter a query"

    else:
        model: QueryModel = get_query_pipeline_from_model()
        model.connect_vector_store()

        results = model.vector_store.similarity_search(
            query=body.q,
            k=5,
            filter=body.filter_json
        )

        return results