import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, Date, Integer, String

from todo import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(512), default='')
    done = Column(Boolean, default=False)
    date = Column(Date, default=None, nullable=True)

    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        date: Optional[datetime.date] = None,
    ) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f'Task <{self.id}>'
