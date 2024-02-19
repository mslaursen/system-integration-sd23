from pydantic import BaseModel, ConfigDict, Field


class BasicModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DataResponse[T: BasicModel](BasicModel):
    data: list[T] | None = None


class DataValueResponse[T: str | int | float | bool](BasicModel):
    data: T | None = None


class _BasePersonDTO(BasicModel):
    name: str
    age: int
    hobbies: list[str] | None = None
    is_married: bool = Field(..., alias="isMarried")


class AddressDTO(BasicModel):
    city: str
    country: str


class PersonDTO(_BasePersonDTO):
    address: AddressDTO


class PersonDTO_CSV(_BasePersonDTO, AddressDTO): ...
