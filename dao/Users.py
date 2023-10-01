from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ProjectsUsers import ProjectsUsers


class UsersInput(SQLModel):
    first_name: str | None = ""
    last_name: str | None = ""
    display_name: str | None = first_name + " " + last_name
    email: str | None = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Users(UsersInput, table=True):
    __tablename__ = "user"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    modified_at: datetime = Field(default_factory=datetime.utcnow)
    projects: List["ProjectsUsers"] | None = Relationship(back_populates="user",
                                                          sa_relationship_kwargs={"cascade": "delete"})

