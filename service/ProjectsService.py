from copy import deepcopy
from datetime import datetime
from typing import Optional

from fastapi import Depends

from dao.Projects import Projects
from repositorties.ProjectsRepository import ProjectsRepository
from repositorties.ProjectDatasetRepository import ProjectDatasetRepository
from repositorties.ProjectUserRepository import ProjectUserRepository
from repositorties.DatasetRepository import DatasetRepository
from dto.DTO import ProjectsDTO, ProjectsOutput
from db import get_session
from sqlmodel import Session


class ProjectsService:
    def __init__(self,
                 projects_repository: ProjectsRepository = Depends(),
                 projects_dataset_repository: ProjectDatasetRepository = Depends(),
                 projects_user_repository: ProjectUserRepository = Depends(),
                 dataset_repository: DatasetRepository = Depends(),
                 session: Session = Depends(get_session)):
        self.projects_repository = projects_repository
        self.projects_dataset_repository = projects_dataset_repository
        self.projects_user_repository = projects_user_repository
        self.dataset_repository = dataset_repository
        self.session = session

    def get_all_projects(self, project_name, offset: int, limit: int):
        return self.projects_repository.get_all_projects(session=self.session, offset=offset,
                                                         limit=limit, project_name=project_name)

    def save_project(self, project: ProjectsDTO) -> ProjectsOutput:
        return self.projects_repository.save_project(session=self.session, project=project)

    def get_project_by_id(self, project_id):
        return self.projects_repository.get_project(project_id=project_id, session=self.session)

    def delete_project(self, project_id):
        self.projects_repository.delete_project(project_id, session=self.session)

    def delete_dataset_from_project(self, project_id, dataset_id):
        project_orm = self.projects_repository.get_project(project_id, session=self.session)
        project_orm.modified_at = datetime.utcnow()
        dataset_orm = self.dataset_repository.get_dataset_by_id(dataset_id=dataset_id, session=self.session)
        project_dataset = [d for d in project_orm.datasets if str(d.dataset_id) == str(dataset_orm.id)][0]
        self.session.delete(project_dataset)

        self.session.commit()

    def update_project_tags(self, project_id, project_tags: dict, project_settings: Optional[dict] = None):
        project_to_update = self.session.get(Projects, project_id)
        existing_tags = deepcopy(project_to_update.tags or {})
        existing_tags.update(project_tags)
        project_to_update.tags = existing_tags

        if project_settings:
            existing_settings = deepcopy(project_to_update.settings or {})
            existing_settings.update(project_settings)
            project_to_update.settings = existing_settings

        project_to_update.modified_at = datetime.utcnow()
        project_to_update.tags['modified_at'] = project_to_update.modified_at.strftime("%m/%d/%Y, %H:%M:%S")

        self.session.commit()
        self.session.refresh(project_to_update)

        project_to_update.datasets = project_to_update.datasets
        project_to_update.users = project_to_update.users

        return project_to_update
