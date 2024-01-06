from pydantic import BaseModel

class Query(BaseModel):
    q: str

class SearchInput(Query):
    filter: dict

class Output(BaseModel):
    output: str
