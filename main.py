from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def simple_func():
    return {"message": 200}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
