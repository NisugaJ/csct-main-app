from chromadb.api.models import Collection
from chromadb.types import Collection

from product_analyzer.components.query_model import QueryModel
from rag.components.rag import RAG_Model

model = QueryModel()


def find_embeddings_by_product_id(id: str  = None):

    model.connect_vector_store()

    collection: Collection = model.chroma_db.get_collection(model.DEFAULT_COLLECTION_NAME)

    embeddings = collection.get(
        include=["documents", "embeddings", "metadatas"],
        where={"product_id": id}
    )

    for emb in embeddings['metadatas']:
        print(emb)
        print("\n\t")


def delete_all_collections():
    for col in model.chroma_db.list_collections():
        model.chroma_db.delete_collection(
            name=col.name,
        )
    print(f"Count after deletion: {len(model.chroma_db.list_collections())}")
