from pathlib import Path

from starlette.staticfiles import StaticFiles

from main import app

print(Path.cwd())
# Public folder
app.mount("/public", StaticFiles(directory=f"{Path.cwd()}/app/public"), name="static")
