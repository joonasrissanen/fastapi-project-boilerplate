from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class PollModel(Base):
    __tablename__ = "polls"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str]

    options: Mapped[List["PollOptionModel"]] = relationship(
        back_populates="poll", cascade="all, delete-orphan"
    )


class PollOptionModel(Base):
    __tablename__ = "poll_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]

    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    poll: Mapped["PollModel"] = relationship(back_populates="options")
