# Entry point for uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web_fetch.app:app", host="0.0.0.0", port=8000, reload=True)