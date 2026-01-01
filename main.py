from fastapi import FastAPI

app = FastAPI(title="Dhakacart API", version="0.1.0")


@app.get("/")
def root():
    return {"message": "Welcome to Dhakacart API!"}


@app.get("/health")
def health():
    return {"status": "healthy"}
