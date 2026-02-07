from fastapi import Path, Query, Body, APIRouter
import uvicorn
from sqlalchemy import insert

from src.database import async_session_maker
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]

@router.get("")
def get_hotels(
    pagination: PaginationDep,
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
    
    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return hotels_


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "sochi", "value": {
        "title": "Отель сочи 5 звезд", 
        "location": "ул. Моря 12"
    }},
    "2": {
        "summary": "dubai", "value": {
            "title": "Отель Дубай у фонтана",
            "location": "ул. Дубай 5"
        }},
    }),
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "ok"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных отеля", description="Тут частично обновляем данные об отели")
def partially_edit_hotel(
    hotel_data: HotelPATCH,
    hotel_id: int = Path(description="Номер отеля которые будет отредактирован частично"),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "ok"}


@router.put("/{hotel_id}")
def edit_hotel(
    hotel_data: Hotel,
    hotel_id: int = Path(description="Номер отеля которые будет отредактирован полностью"),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "ok"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app")
