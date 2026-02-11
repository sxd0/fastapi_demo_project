from fastapi import Path, APIRouter
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.hotels import HotelAdd, HotelPATCH


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_me_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )

    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "ok", "data": booking}


@router.patch("/{hotel_id}", summary="Частичное обновление данных отеля", description="Тут частично обновляем данные об отели")
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
