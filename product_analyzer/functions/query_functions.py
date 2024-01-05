from product_analyzer.components.query_model import QueryModel
from product_analyzer.utils.db import get_db


def get_query_model():

    # Initialize a QueryModel instance with the chroma db connection and embedding function
    query_model = QueryModel(db=get_db())

    return query_model
