from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str = Field(min_length = 1, max_length = 100)
    email: str
    password: str = Field(min_length = 8, max_length = 255)



class UserResponse(BaseModel):
    id: int
    name: str
    email: str


    model_config = ConfigDict(from_attributes=True)
