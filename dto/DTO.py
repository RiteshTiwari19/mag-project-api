from datetime import datetime
from typing import Optional, List
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from dao.Dataset import Dataset
from dao.ProjectDataset import ProjectDatasetInputDAO
from dao.ProjectsUsers import ProjectUserInputDAO
from dao.Users import UsersInput
from dao.Projects import Projects
from dao.Dataset import DatasetInput
from dao.DatasetType import DatasetType

if TYPE_CHECKING:
    from dao.Users import Users


class DatasetTypeDTO(BaseModel):
    name: str | None
    description: str | None


class DatasetDTO(BaseModel):
    name: str | None
    id: UUID | None
    path: str | None
    parent_dataset_id: UUID | None
    snap: Optional[str] = None
    tags: Optional[dict] = None
    created_at: datetime | None
    dataset_type_id: UUID | None
    project_id: UUID | None


class ProjectDatasetInput(BaseModel):
    dataset: DatasetDTO | None = None
    project_dataset_state: str | None = "INIT"


class ProjectsDTO(BaseModel):
    class UserProjectRole(BaseModel):
        role: str = None
        user_id: UUID = None

    name: str | None
    tags: dict | None
    created_at: datetime | None
    dataset: ProjectDatasetInput | None
    user_role: List[UserProjectRole] = None


class DatasetExtended(DatasetDTO):
    dataset_type: Optional[DatasetType]


class ProjectDatasetDTO(ProjectDatasetInputDAO):
    dataset: DatasetExtended


class DatasetProjectDTO(ProjectDatasetInputDAO):
    project: Projects


class ProjectDTO(BaseModel):
    name: str | None
    tags: dict | None
    created_at: datetime | None


class ProjectUserDTO(ProjectUserInputDAO):
    project: ProjectDTO


class UsersDTO(UsersInput):
    pass


class UsersResponseDTO(UsersDTO):
    id: UUID | None


class UserInProject(ProjectUserInputDAO):
    user: UsersResponseDTO


class ProjectsOutput(BaseModel):
    id: UUID
    name: str | None
    tags: dict | None
    settings: dict | None
    created_at: datetime | None
    modified_at: datetime | None
    datasets: List[ProjectDatasetDTO] | None
    users: List[UserInProject] | None


class DatasetsOutput(DatasetInput):
    id: UUID
    modified_at: datetime | None
    projects: List[DatasetProjectDTO] | None


class DatasetsWithDatasetTypeDTO(DatasetsOutput):
    dataset_type: DatasetType | None


class UserResponseDatasetsDTO(UsersResponseDTO):
    projects: List[ProjectUserDTO] | None


class UserFilterRequest(BaseModel):
    emails: List[str] | None = []
    first_names: List[str] | None = []


class DatasetTypeFilterDTO(BaseModel):
    names: List[str] | None = []


class ProjectTagsDTO(BaseModel):
    tags: dict = {}
    settings: Optional[dict] = None


class DatasetUpdateDTO(BaseModel):
    tags: Optional[dict]
    name: str | None
    path: str | None
