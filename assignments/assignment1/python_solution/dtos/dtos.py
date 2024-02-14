from pydanic import BaseModel


class AddressDTO(BaseModel):
    city: str
    street: str


class PersonDTO(BaseModel):
    name: str
    age: int
    address: AddressDTO
    hobbies: list[str]
    is_married: bool
