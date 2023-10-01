from typing import List
from uuid import UUID
from datetime import datetime

from fastapi import Depends
from sqlmodel import Session, select, col
from sqlalchemy.orm import joinedload

from repositorties.DatasetRepository import DatasetRepository
from repositorties.ProjectDatasetRepository import ProjectDatasetRepository
from repositorties.UserRepository import UserRepository
from repositorties.ProjectUserRepository import ProjectUserRepository
from dao.Projects import Projects
from dto.DTO import ProjectsOutput, ProjectsDTO


class ProjectsRepository:

    def __init__(self, dataset_repository: DatasetRepository = Depends(),
                 project_dataset_repository: ProjectDatasetRepository = Depends(),
                 user_repository: UserRepository = Depends(),
                 project_user_repository: ProjectUserRepository = Depends()):
        self.dataset_repository = dataset_repository
        self.project_dataset_repository = project_dataset_repository
        self.user_repository = user_repository
        self.project_user_repository = project_user_repository

    def get_all_projects(self, project_name, session: Session, offset: int = -1, limit: int = -1) -> List[ProjectsOutput] | List:

        project_name_query = f'%{project_name or ""}%'
        query = select(Projects).where(col(Projects.name).ilike(project_name_query))

        if offset >= 0 and limit >= 0:
            query = query.offset(offset).limit(limit)

        query = query.options(joinedload(Projects.datasets))\
            .options(joinedload(Projects.users))
        out = session.execute(query).unique().scalars().all()
        return out

    def save_project(self, session, project: ProjectsDTO) -> ProjectsOutput:
        project_orm = Projects.from_orm(project)
        project_orm.tags = project_orm.tags or {}
        project_orm.tags['name'] = project_orm.name
        project_orm.tags['created_at'] = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
        project_orm.tags['modified_at'] = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
        session.add(project_orm)

        if project.user_role:
            for user_role in project.user_role:
                user_orm = self.user_repository.get_user_by_id(user_id=user_role.user_id)
                self.project_user_repository \
                    .save_project_user_link(user=user_orm, project=project_orm, role=user_role.role, session=session)

        if project.dataset and project.dataset.dataset:
            dataset_orm = self.dataset_repository.add_new_dataset(dataset=project.dataset, session=session)
            dataset_link_orm = self.project_dataset_repository.save_project_dataset_link(
                project=project_orm,
                dataset=dataset_orm,
                project_dataset_state=project.dataset.project_dataset_state,
                session=session)

        session.commit()
        session.refresh(project_orm)
        project_orm.datasets = project_orm.datasets
        project_orm.users = project_orm.users
        return project_orm

    def get_project(self, project_id, session: Session):
        project = session.get(Projects, project_id)
        project.datasets = project.datasets
        for dts in project.datasets:
            dts.dataset.dataset_type = dts.dataset.dataset_type
        project.users = project.users
        return project

    def delete_project(self, project_id: UUID, session: Session):
        project_to_delete = self.get_project(project_id, session)
        session.delete(project_to_delete)
        session.commit()
