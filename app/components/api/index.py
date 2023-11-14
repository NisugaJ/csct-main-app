from supermarketscraper.main import app


@app.get("/test")
def read_root():
    """
    Handler function for the root endpoint.

    Returns:
        dict: The response containing the app name.
    """
    return {"app": "test"}
