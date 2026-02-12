from datetime import date
from fastapi import Path, Query, Body, APIRouter

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelAdd, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: int | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(examples=["2024-08-01"]),
    date_to: date = Query(examples=["2024-08-10"]),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page or 5,
        offset=per_page * (pagination.page - 1),
    )


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "sochi",
                "value": {
                    "title": "Отель у моря 5 звезд",
                    "location": "Сочи, ул. Моря 12",
                },
            },
            "2": {
                "summary": "dubai",
                "value": {"title": "Отель у фонтана", "location": "Дубай, ул. Дубай 5"},
            },
        }
    ),
):

    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "ok", "data": hotel}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных отеля",
    description="Тут частично обновляем данные об отели",
)
async def partially_edit_hotel(
    db: DBDep,
    hotel_data: HotelPATCH,
    hotel_id: int = Path(description="Номер отеля которые будет отредактирован частично"),
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.put("/{hotel_id}")
async def edit_hotel(
    db: DBDep,
    hotel_data: HotelAdd,
    hotel_id: int = Path(description="Номер отеля которые будет отредактирован полностью"),
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "ok"}
