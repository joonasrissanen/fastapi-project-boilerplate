from pydantic import BaseModel, ConfigDict


class PollOptionBase(BaseModel):
    text: str
    model_config = ConfigDict(from_attributes=True)


class PollOptionCreate(PollOptionBase):
    pass


class PollOption(PollOptionBase):
    id: int


class PollBase(BaseModel):
    question: str
    model_config = ConfigDict(from_attributes=True)


class PollCreate(PollBase):
    options: list[PollOptionCreate]


class Poll(PollBase):
    id: int
    options: list[PollOption]
