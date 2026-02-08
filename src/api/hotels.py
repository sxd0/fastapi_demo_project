from fastapi import Path, Query, Body, APIRouter
import uvicorn

from src.database import async_session_maker
from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    location: int | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page or 5,
            offset=per_page * (pagination.page - 1)
        )


@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "sochi", "value": {
        "title": "Отель у моря 5 звезд", 
        "location": "Сочи, ул. Моря 12"
    }},
    "2": {
        "summary": "dubai", "value": {
            "title": "Отель у фонтана",
            "location": "Дубай, ул. Дубай 5"
        }},
    }),
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "ok", "data": hotel}


@router.patch("/{hotel_id}", summary="Частичное обновление данных отеля", description="Тут частично обновляем данные об отели")
async def partially_edit_hotel(
    hotel_data: HotelPATCH,
    hotel_id: int = Path(description="Номер отеля которые будет отредактирован частично"),
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "ok"}


@router.put("/{hotel_id}")
async def edit_hotel(
    hotel_data: HotelAdd,
    hotel_id: int = Path(description="Номер отеля которые будет отредактирован полностью"),
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "ok"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "ok"}
