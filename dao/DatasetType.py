from uuid import UUID, uuid4
from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .Dataset import Dataset


class DatasetTypeInput(SQLModel):
    name: str | None = Field(unique=True)
    description: str | None


class DatasetType(DatasetTypeInput, table=True):
    __tablename__ = "dataset_type"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    datasets: List["Dataset"] | None = Relationship(back_populates="dataset_type")
