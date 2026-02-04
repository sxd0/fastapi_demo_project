from fastapi import FastAPI, Path, Query, Body
import uvicorn

from hotels import router as router_hotels


app = FastAPI()

app.include_router(router_hotels)


@app.get("/")
def simple_func():
    return {"message": 200}


if __name__ == "__main__":
    uvicorn.run("main:app")
