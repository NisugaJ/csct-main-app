import os

from product_analyzer.components.query_model import QueryModel
from product_analyzer.utils.db import get_db


def prepare_vector_store():
    db = get_db()
    pre_delete_collection = True \
        if os.environ.get("PRE_DELETE_COLLECTION") == "True" \
        else False
    relative_data_dir = os.environ.get("RELATIVE_DATA_DIR")

    query_model = QueryModel(db=db, pre_delete_collection=pre_delete_collection)
    query_model.add_json_docs_to_vector_store(relative_data_dir=relative_data_dir)

