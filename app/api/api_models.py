from pydantic import BaseModel

class Query(BaseModel):
    q: str

class SearchInput(Query):
    filter: dict or None

class Output(BaseModel):
    output: str
