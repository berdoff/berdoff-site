from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def mainn():
    return "1"