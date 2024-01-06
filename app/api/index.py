import asyncio
from pathlib import Path
from typing import AsyncIterable

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles

from app.api.api_models import SearchInput, Query
from product_analyzer.components.query_model import QueryModel
from product_analyzer.functions.query_functions import get_query_model
from rag.components.rag import RAG_Model
from rag.functions.rag_pipeline import get_rag_pipeline_from_model

app_router = APIRouter()

# Public folder
app_router.mount("/public", StaticFiles(directory=f"{Path.cwd()}/app/public"), name="static")



@app_router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app_router.post("/search")
async def get_answers(body: SearchInput):
    query_text = body.q
    print(body.filter)
    q_filter = body.filter if body.filter is not None else {}

    if query_text == "" or query_text is None:
        return "Please enter a query"
    else:
        model: QueryModel = get_query_model()
        model.connect_vector_store()

        results = model.vector_store.similarity_search(
            query=body.q,
            k=10,
            filter=q_filter
        )

        return results


@app_router.post("/query")
async def get_answers(query: Query):
    query_text = query.q
    if query_text == "" or query_text is None:
        return "Please enter a query"

    else:
        model: RAG_Model = get_rag_pipeline_from_model()

        async def send_token(content) -> AsyncIterable[str]:

            async def coroutine_wrapper(async_gen, args):
                try:
                    async for i in async_gen(args):
                        pass
                except ValueError:
                    print(
                        tuple(
                            [(i, j) async for i, j in async_gen(
                                args
                                )]
                            )
                        )

            task = asyncio.create_task(
                coroutine_wrapper(model.rag_pipeline.astream, content)
            )

            try:
                async for token in model.llm_callback.aiter():
                    yield token
            except Exception as e:
                print(
                    f"Caught exception: {e}"
                    )
            finally:
                model.llm_callback.done.set()

            await task

        return StreamingResponse(
            send_token(content=query_text),
            media_type="text/event-stream"
        )
