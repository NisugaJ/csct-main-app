from product_analyzer.components.query_model import QueryModel
from product_analyzer.utils.db import get_db


def chroma_run():
    model = QueryModel()
    model.connect_vector_store()

    # Fetch the embedding for that product
    # product = products.get(
    #     ids=["ASDA_1000383171038"],
    #     include=["embeddings"]
    #     )
    # print(product)

    results = model.vector_store.similarity_search(
        query="rice flour sausage",
        k=5,
    )

    for r in results:
        print(r)


    # results = model.chroma_db.get_collection("products").query(
    #     query_texts=["olive"],
    #     n_results=10,
    # )
    #
    # [print(r) for r in results]
