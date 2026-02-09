from src.models.bookings import BookingsOrm
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking
from src.schemas.hotels import Hotel


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
