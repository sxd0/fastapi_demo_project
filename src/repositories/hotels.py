from sqlalchemy import select
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
        self,
        location,
        title,
        limit,
        offset,
    ):
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

        return result.scalars().all()
