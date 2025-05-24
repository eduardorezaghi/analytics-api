from fastapi import FastAPI, Depends

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}
