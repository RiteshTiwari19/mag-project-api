from typing import TYPE_CHECKING
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

if TYPE_CHECKING:
    from .Projects import Projects
    from .Dataset import Dataset


class ProjectDatasetInputDAO(SQLModel):
    project_dataset_state = "INIT"


class ProjectDataset(ProjectDatasetInputDAO, table=True):
    __tablename__ = "project_dataset"

    project_id: Optional[UUID] = Field(
        default=None, foreign_key="project.id", primary_key=True
    )
    dataset_id: Optional[UUID] = Field(
        default=None, foreign_key="dataset.id", primary_key=True
    )

    project: "Projects" = Relationship(back_populates="datasets")
    dataset: "Dataset" = Relationship(back_populates="projects")


