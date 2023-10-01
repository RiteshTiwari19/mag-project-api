from typing import Optional, TYPE_CHECKING
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .Projects import Projects
    from .Users import Users


class ProjectUserInputDAO(SQLModel):
    role: str | None = "CONTRIBUTOR"


class ProjectsUsers(ProjectUserInputDAO, table=True):
    __tablename__ = "project_user"

    project_id: Optional[UUID] = Field(
        default=None, foreign_key="project.id", primary_key=True
    )
    user_id: Optional[UUID] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )

    project: "Projects" = Relationship(back_populates="users")
    user: "Users" = Relationship(back_populates="projects")
