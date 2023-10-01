from typing import List
from uuid import UUID

from fastapi import APIRouter, Body

from auth.jwt_bearer import JwtBearer
from service.DatasetService import DatasetService
from service.ProjectsService import ProjectsService
from fastapi import Depends
from dto.DTO import ProjectsDTO, ProjectsOutput, ProjectDatasetInput, DatasetsOutput, UserResponseDatasetsDTO, \
    ProjectTagsDTO
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED

from service.UserService import UserService

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])


@router.get("/", response_model=List[ProjectsOutput], dependencies=[Depends(JwtBearer())])
def get_projects(project_name: str | None = None, offset: int | None = 0, limit: int | None = 10,
                 projects_service: ProjectsService = Depends()):
    projects = projects_service.get_all_projects(project_name=project_name, offset=offset, limit=limit)
    return projects


@router.get("/{project_id}", response_model=ProjectsOutput, dependencies=[Depends(JwtBearer())])
def get_project_by_id(project_id: UUID, projects_service: ProjectsService = Depends()):
    project = projects_service.get_project_by_id(project_id)
    return project


@router.put("/{project_id}", status_code=HTTP_202_ACCEPTED, response_model=ProjectsOutput,
            dependencies=[Depends(JwtBearer())])
def update_project_tags(project_id: UUID, project_tags: ProjectTagsDTO = Body(),
                        projects_service: ProjectsService = Depends()):
    updated_project = projects_service.update_project_tags(project_id, project_tags.tags, project_tags.settings)
    return updated_project


@router.delete("/{project_id}", status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(JwtBearer())])
def delete_project(project_id: UUID, projects_service: ProjectsService = Depends()):
    projects_service.delete_project(project_id)


@router.post("/", status_code=HTTP_201_CREATED, dependencies=[Depends(JwtBearer())])
def create_new_project(project: ProjectsDTO, projects_service: ProjectsService = Depends()) -> ProjectsOutput:
    project = projects_service.save_project(project)
    return project


@router.post("/{project_id}/datasets/{dataset_id}", status_code=HTTP_201_CREATED, dependencies=[Depends(JwtBearer())],
             response_model=DatasetsOutput)
def add_existing_dataset_to_project(project_id: UUID, dataset_id: UUID, project_dataset_state: str,
                                    dataset_service: DatasetService = Depends()):
    saved_dataset = dataset_service.create_new_dataset(project_id=project_id, dataset_id=dataset_id,
                                                       project_dataset_state=project_dataset_state)
    return saved_dataset


@router.post("/{project_id}/users/{user_id}", status_code=HTTP_201_CREATED, dependencies=[Depends(JwtBearer())],
             response_model=UserResponseDatasetsDTO)
def add_existing_user_to_project(project_id: UUID, user_id: UUID, user_role: str,
                                 user_service: UserService = Depends()):
    saved_user = user_service.add_user_to_project(project_id=project_id, user_id=user_id,
                                                  user_role=user_role)
    return saved_user


@router.get("/{project_id}/users/", status_code=HTTP_200_OK, dependencies=[Depends(JwtBearer())],
            response_model=List[UserResponseDatasetsDTO])
def get_project_users(project_id: UUID, user_service: UserService = Depends()):
    project_users = user_service.get_project_users(project_id=project_id)
    return project_users


@router.delete("/{project_id}/datasets/{dataset_id}", status_code=HTTP_204_NO_CONTENT,
               dependencies=[Depends(JwtBearer())])
def remove_dataset_from_project(project_id: UUID, dataset_id: UUID,
                                dataset_service: DatasetService = Depends(),
                                project_service: ProjectsService = Depends()):
    project_service.delete_dataset_from_project(project_id=project_id, dataset_id=dataset_id)
