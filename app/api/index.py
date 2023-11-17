from starlette.staticfiles import StaticFiles

from main import app

# Public folder
app.mount("/public", StaticFiles(directory="/main-app/app/public"), name="static")
