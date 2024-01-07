from product_analyzer.utils.db import get_db
from rag.components.rag import RAG_Model


def get_rag_pipeline_from_model():

    # Initialize a RAG_Model instance with the chroma db connection and embedding function
    rag = RAG_Model(db=get_db())

    # Connect to the vector store
    rag.connect_vector_store()

    # Build the RAG pipeline
    rag.build_pipeline()

    # # Run the pipeline and get query response
    # answer = rag.get_response(query)
    #
    # return answer

    return rag

# Basic RAG Pipeline - without OOP

#
# def run_pipeline(query):
#
#     loader = WebBaseLoader(
#         # web_path="https://en.wikipedia.org/wiki/Extended_producer_responsibility",
#         web_path="https://en.wikipedia.org/wiki/Aerodynamics",
#         bs_kwargs=dict(
#             parse_only=bs4.SoupStrainer(
#                 class_=("mw-body-content", "mw-page-title-main")
#             ),
#         ), )
#     docs = loader.load()
#
#     print(len(docs[0].page_content))
#
#
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200
#     )
#     splits = text_splitter.split_documents(
#         docs
#         )
#     splits = splits[:2]
#
#     chroma_client = HttpClient()
#
#     collection_name = "epr_documents"
#     openai_key = os.environ.get("OPENAI_API_KEY")
#     embedding_function = embedding_functions.OpenAIEmbeddingFunction(
#         api_key=openai_key
#     )
#
#     collection = chroma_client.get_or_create_collection(name=collection_name, embedding_function=embedding_function)
#     collection.add(
#         documents=[item.page_content for item in splits],
#         ids=[str(i) for i in range(len(splits))],
#     )
#
#     vectorstore = Chroma.from_documents(
#         documents=splits,
#         embedding=OpenAIEmbeddings(),
#         client=chroma_client,
#         collection_name=collection_name
#     )
#
#     print(f"There are ", vectorstore._collection.count(), "in the collection")
#
#     retriever = vectorstore.as_retriever()
#
#     prompt = hub.pull(
#         "rlm/rag-prompt"
#         )
#
#     llm = ChatOpenAI(
#         model_name="gpt-3.5-turbo",
#         temperature=0
#         )
#
#     def format_docs(docs):
#         formatted_doc = "\n\n".join(
#             doc.page_content for doc in docs
#             )
#         return formatted_doc
#
#     rag_chain = (
#             {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())
#
#     answer = rag_chain.invoke(
#         query
#     )
#
#     return answer