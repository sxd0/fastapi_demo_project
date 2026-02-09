from datetime import date
from fastapi import APIRouter
from fastapi import Path, Query, Body, APIRouter
from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPATCHRequest


router = APIRouter(prefix="/rooms", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example=["2024-08-01"]),
        date_to: date = Query(example=["2024-08-10"]),
    ):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, db: DBDep, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_rooms(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "ok", "data": room}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int,
    db: DBDep,
    room_id: int,
    room_data: RoomPATCHRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id, db: DBDep, room_id, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, db: DBDep, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ok"}
