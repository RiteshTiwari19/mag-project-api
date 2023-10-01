from datetime import datetime
from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, JSON, Column, Relationship

from dao.ProjectDataset import ProjectDataset

if TYPE_CHECKING:
    from .ProjectsUsers import ProjectsUsers
    from .ProjectDataset import ProjectDataset


class ProjectsInput(SQLModel):
    name: str | None = ""
    tags: dict | None = Field(default={'name': name}, sa_column=Column(JSON))
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    settings: dict | None = Field(default={'ambient_constant': 500}, sa_column=Column(JSON))


class Projects(ProjectsInput, table=True):
    __tablename__ = "project"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    modified_at: datetime = Field(default_factory=datetime.utcnow)
    users: List["ProjectsUsers"] | None = Relationship(back_populates="project",
                                                       sa_relationship_kwargs={"cascade": "delete"})
    datasets: List["ProjectDataset"] | None = Relationship(back_populates="project",
                                                           sa_relationship_kwargs={"cascade": "delete"})
