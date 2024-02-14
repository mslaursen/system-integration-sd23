from pydantic import BaseModel, Field


class _BasePersonDTO(BaseModel):
    name: str
    age: int
    hobbies: list[str] | None = None
    is_married: bool = Field(..., alias="isMarried")


class AddressDTO(BaseModel):
    city: str
    country: str


class PersonDTO(_BasePersonDTO):
    address: AddressDTO


class PersonDTO_CSV(_BasePersonDTO, AddressDTO): ...
