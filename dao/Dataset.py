from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from typing import Optional

if TYPE_CHECKING:
    from .DatasetType import DatasetType
    from .ProjectDataset import ProjectDataset


class DatasetInput(SQLModel):
    parent_dataset_id: UUID | None
    name: str | None = ""
    path: str | None
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    snap: str | None
    tags: Optional[dict] = Field(default={'name': name}, sa_column=Column(JSON))


class Dataset(DatasetInput, table=True):
    __tablename__ = "dataset"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    dataset_type_id: UUID | None = Field(default=None, foreign_key="dataset_type.id")
    modified_at: datetime = Field(default_factory=datetime.utcnow)
    projects: List["ProjectDataset"] | None = Relationship(back_populates="dataset", sa_relationship_kwargs={"cascade": "delete"})
    dataset_type: Optional["DatasetType"] = Relationship(back_populates="datasets")


