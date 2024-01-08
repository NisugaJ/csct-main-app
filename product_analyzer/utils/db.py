import os

import chromadb
from chromadb import HttpClient, Settings
from codetiming import Timer

settings = Settings(chroma_api_impl="chromadb.api.fastapi.FastAPI", allow_reset=True, anonymized_telemetry=False)

host = os.getenv("chroma_server_host")
port = os.getenv("chroma_server_http_port")

chroma_db = chromadb.PersistentClient(path="/home/csct-admin/chromadb/db")

print(f"ChromaDB Healthcheck: {chroma_db.heartbeat()}")  # this should work with or without authentication - it is a public endpoint
print(f"Chroma_db version: {chroma_db.get_version()}")  # this should work with or without authentication - it is a public endpoint
print(f"Collection count: {len(chroma_db.list_collections())}")  # this is a protected endpoint and requires authentication

@Timer(
    name="utils.db.get_db",
    text="{name}: {:.4f} seconds"
    )
def get_db():
    return chroma_db
