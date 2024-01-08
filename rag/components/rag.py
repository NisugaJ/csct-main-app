import json
import os
from typing import List

from chromadb import PersistentClient
from codetiming import Timer

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import StrOutputParser
from langchain.vectorstores.chroma import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough

from app.models.product.Product import Product
from product_analyzer.utils.db import get_db
from product_analyzer.utils.document import get_doc_from_raw
from rag.components.prompt_template import planta_prompt_template
from utils.files import get_files_in_dir


def format_docs(docs):
    formatted_doc = "\n\n".join(
        doc.page_content for doc in docs
        )
    return formatted_doc


class RAG_Model:
    DEFAULT_COLLECTION_NAME: str = os.environ.get("CHAT_COLLECTION_NAME")

    def __init__(
        self,
        db: PersistentClient or None = None,
        pre_delete_collection: bool = False
    ):
        self.__openai_key = os.environ.get("OPENAI_API_KEY")

        self.docs = []
        self.split_docs = []
        self.embeddings_model = OpenAIEmbeddings()
        self.collection = None
        self.chroma_db: PersistentClient = db
        self.vector_store: Chroma = None

        self.prompt = None
        self.llm = None

        self.retriever = None
        self.rag_pipeline = None

        self.llm_callback = AsyncIteratorCallbackHandler()

        if self.chroma_db is None:
            self.connect_chroma_db()

        if pre_delete_collection == "True":
            self.delete_current_collection()
            print(f"Deleted existing collection {self.DEFAULT_COLLECTION_NAME}")

    def delete_current_collection(self):
        if self.DEFAULT_COLLECTION_NAME in self.chroma_db.list_collections():
            self.chroma_db.delete_collection(
                name=self.DEFAULT_COLLECTION_NAME
            )

    def connect_chroma_db(self):
        self.chroma_db = get_db()

    @Timer(name="connect_vector_store", text="{name}: {:.4f} seconds")
    def connect_vector_store(self):
        self.vector_store = Chroma(
            collection_name=self.DEFAULT_COLLECTION_NAME,
            client=self.chroma_db,
            embedding_function=OpenAIEmbeddings(),
        )

    @Timer(name="build_vector_store", text="{name}: {:.4f} seconds")
    def build_vector_store(self, collection_name=DEFAULT_COLLECTION_NAME):
        self.vector_store = Chroma.from_documents(
            documents=self.docs,
            ids=[f"id_{i}" for i in range(
                len(
                    self.docs
                    )
                )],
            embedding=OpenAIEmbeddings(),
            client=self.chroma_db,
            collection_name=collection_name,
            collection_metadata={"hnsw:space": "cosine"}
        )

    def load_json_docs(self, file_paths: List[str]):
        for f_path in file_paths:
            with open(f_path) as f:
                raw_docs = json.load(f)

                for raw_doc in raw_docs:
                    raw_doc.pop("_id")
                    doc = get_doc_from_raw(Product(**raw_doc), use_case="chat")
                    self.docs.append(doc)


    def build_pipeline(self):

        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0,
            streaming=True,
            verbose=True,
            callbacks=[self.llm_callback]
        )

        self.retriever = self.vector_store.as_retriever()

        self.rag_pipeline = (
                {
                    "context": self.retriever | format_docs,
                    "question": RunnablePassthrough()
                } |
                planta_prompt_template |
                self.llm |
                StrOutputParser()
        )

    def add_json_docs_to_vector_store(self, relative_data_dir="./data"):

        all_files = get_files_in_dir(relative_dir=relative_data_dir, file_ext=".json")

        self.load_json_docs(
            all_files
            )
        self.build_vector_store()

    def get_response(self, query):
        return self.rag_pipeline.invoke(query)