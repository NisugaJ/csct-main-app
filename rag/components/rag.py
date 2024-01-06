import os

from chromadb import HttpClient
from codetiming import Timer

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import StrOutputParser
from langchain.vectorstores.chroma import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough

from rag.components.prompt_template import planta_prompt_template


def format_docs(docs):
    formatted_doc = "\n\n".join(
        doc.page_content for doc in docs
        )
    return formatted_doc


class RAG_Model:
    DEFAULT_COLLECTION_NAME: str = os.environ.get("DEFAULT_COLLECTION_NAME")

    def __init__(
        self,
        db_conn: HttpClient or None = None,
    ):
        self.__openai_key = os.environ.get("OPENAI_API_KEY")

        self.docs = []
        self.split_docs = []
        self.embeddings_model = OpenAIEmbeddings()
        self.collection = None
        self.db_conn: HttpClient = db_conn
        self.vector_store: Chroma = None

        self.prompt = None
        self.llm = None

        self.retriever = None
        self.rag_pipeline = None

        self.llm_callback = AsyncIteratorCallbackHandler()

        self.connect_vector_store()

    @Timer(name="connect_vector_store", text="{name}: {:.4f} seconds")
    def connect_vector_store(self):
        self.vector_store = Chroma(
            collection_name=self.DEFAULT_COLLECTION_NAME,
            client=self.db_conn,
            embedding_function=OpenAIEmbeddings(),
        )

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

    def get_response(self, query):
        return self.rag_pipeline.invoke(query)