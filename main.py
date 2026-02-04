from fastapi import FastAPI, Path, Query, Body
import uvicorn

app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]

@app.get("/hotels")
def get_hotels(
    id: int | None = Query(None, description="Айди"),
    title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.get("/")
def simple_func():
    return {"message": 200}


@app.post("/hotels")
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
    })
    return {"status": "ok"}


@app.patch("/hotels/{hotel_id}", summary="Частичное обновление данных отеля", description="Тут частично обновляем данные об отели")
def partially_edit_hotel(
    hotel_id: int = Path(description="Номер отеля которые будет отредактирован частично"),
    title: str | None = Body(None, description="Название"),
    name: str | None = Body(None, description="Имя"),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "ok"}


@app.put("/hotels/{hotel_id}")
def edit_hotel(
    hotel_id: int = Path(description="Номер отеля которые будет отредактирован полностью"),
    title: str = Body(description="Название"),
    name: str = Body(description="Имя"),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "ok"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app")
