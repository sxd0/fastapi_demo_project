from pydantic import BaseModel, ConfigDict, Field


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPATCHRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


class RoomPATCH(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
