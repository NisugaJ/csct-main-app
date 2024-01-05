import json
import os
from typing import List, Iterable

from chromadb import HttpClient, Documents
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions import HuggingFaceEmbeddingFunction

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, SentenceTransformerEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore

from app.models.product.Product import Product
from product_analyzer.utils.db import get_db
from product_analyzer.utils.document import get_doc_from_raw


def format_docs(docs):
    formatted_doc = "\n\n".join(
        doc.page_content for doc in docs
        )
    return formatted_doc


class QueryModel:
    DEFAULT_COLLECTION_NAME: str = "products_v2"

    def __init__(self, db=None, pre_delete_collection: bool = False):
        self.__hf_key = os.environ.get(
            "HUGGINGFACEHUB_API_TOKEN"
            )
        self.__openai_key = os.environ.get(
            "OPENAI_API_KEY"
        )

        self.docs: Documents = []
        self.split_docs: Iterable(Document) = None
        self.chroma_db: HttpClient = db
        self.embedding_function = None
        self.collection = None
        self.vector_store: VectorStore = None

        self.prompt = None
        self.llm = None

        self.retriever = None
        self.rag_pipeline = None

        if self.chroma_db is None:
            self.connect_chroma_db()

        if pre_delete_collection:
            self.delete_current_collection()
            print(f"Deleted existing collection {self.DEFAULT_COLLECTION_NAME}")

        self.set_embedding_function()

    def delete_current_collection(self):
        if self.DEFAULT_COLLECTION_NAME in self.chroma_db.list_collections():
            self.chroma_db.delete_collection(
                name=self.DEFAULT_COLLECTION_NAME
            )

    def load_json_docs(self, file_paths: List[str]):
        for f_path in file_paths:
            with open(f_path) as f:
                raw_docs = json.load(f)

                for raw_doc in raw_docs:
                    raw_doc.pop("_id")
                    doc = get_doc_from_raw(Product(**raw_doc))
                    self.docs.append(doc)

                print(self.docs[0])

    def run_docs_splitter(self):
        if not len(self.docs) > 0:
            raise ValueError("No documents to split")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=256,
            chunk_overlap=20
        )
        self.split_docs = text_splitter.split_documents(self.docs)

    def connect_chroma_db(self):
        self.chroma_db = get_db()

    def set_embedding_function(self):
        # self.embedding_function = SentenceTransformerEmbeddings(
        #     model_name="sentence-transformers/all-mpnet-base-v2",
        # )
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=self.__openai_key
        )

    def get_or_create_collection(self, collection_name=DEFAULT_COLLECTION_NAME):
        self.collection = self.chroma_db.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
        )

    def add_docs_to_collection(self, docs=None):
        docs_ = self.docs
        if docs is not None:
            docs_ = docs

        self.collection.add(
            documents=[item.page_content for item in docs_],
            ids=[item.metadata["product_id"] for item in docs_],
            metadatas=[item.metadata for item in docs_]
        )

        print(f"Now There are {self.vector_store._collection.count()} in the collection")

    def add_split_docs_to_collection(self, split_docs=None):
        docs_ = self.split_docs
        if split_docs is not None:
            docs_ = split_docs

        self.collection.add(
            documents=[item.page_content for item in docs_],
            ids=[f"id_{i}" for i in range(len(docs_))],
            metadatas=[item.metadata for item in docs_],
        )

    def build_vector_store(self, collection_name=DEFAULT_COLLECTION_NAME):
        self.vector_store = Chroma.from_documents(
            documents=self.split_docs,
            ids=[f"id_{i}" for i in range(len(self.split_docs))],
            embedding=OpenAIEmbeddings(),
            client=self.chroma_db,
            collection_name=collection_name
        )

    def connect_vector_store(self):
        self.vector_store = Chroma(
            client=self.chroma_db,
            embedding_function=OpenAIEmbeddings(),
            collection_name=self.DEFAULT_COLLECTION_NAME
        )


    def build_pipeline(self):

        pass

    def get_response(self, query):
        return self.rag_pipeline.invoke(query)

    def add_json_docs_to_vector_store(self, relative_data_dir="./data"):

        all_files = []

        for filename in os.listdir(relative_data_dir):
            file = f"{relative_data_dir}/{filename}"
            _, file_extension = os.path.splitext(file)
            if file_extension == ".json":
                all_files.append(file)

        self.load_json_docs(all_files)
        self.run_docs_splitter()
        self.build_vector_store()
