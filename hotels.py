from fastapi import Path, Query, Body, APIRouter
import uvicorn

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]

@router.get("/")
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


@router.post("/")
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
    })
    return {"status": "ok"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных отеля", description="Тут частично обновляем данные об отели")
def partially_edit_hotel(
    hotel_id: int = Path(description="Номер отеля которые будет отредактирован частично"),
    title: str | None = Body(None, description="Название"),
    name: str | None = Body(None, description="Имя"),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "ok"}


@router.put("/{hotel_id}")
def edit_hotel(
    hotel_id: int = Path(description="Номер отеля которые будет отредактирован полностью"),
    title: str = Body(description="Название"),
    name: str = Body(description="Имя"),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "ok"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app")
