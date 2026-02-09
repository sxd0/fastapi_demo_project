from datetime import date
from sqlalchemy import select
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
        self,
        location,
        title,
        limit,
        offset,
    ) -> list[Hotel]:
        query = select(HotelsOrm)
        if location:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [self.schema.model_validate(hotel) for hotel in result.scalars().all()]


    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        return await self.get_filtered(HotelsOrm.id.in_(rooms_ids_to_get))
