from fastapi import Path, Query, Body, APIRouter
import uvicorn
from sqlalchemy import insert, select

from src.database import async_session_maker
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="Айди"),
    title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)

        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)

        hotels = result.scalars().all()
        return hotels


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
