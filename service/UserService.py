import datetime
from uuid import UUID
from typing import List

from fastapi import Depends
from sqlmodel import Session

from repositorties.UserRepository import UserRepository
from repositorties.ProjectUserRepository import ProjectUserRepository
from repositorties.ProjectsRepository import ProjectsRepository
from dto.DTO import UsersResponseDTO, UsersDTO, UserResponseDatasetsDTO
from db import get_session


class UserService:
    def __init__(self, users_repository: UserRepository = Depends(),
                 project_user_repository: ProjectUserRepository = Depends(),
                 project_repository: ProjectsRepository = Depends(),
                 session: Session = Depends(get_session)):
        self.users_repository = users_repository
        self.project_user_repository = project_user_repository
        self.project_repository = project_repository
        self.session = session

    def save_user(self, user: UsersDTO) -> UsersResponseDTO:
        return self.users_repository.add_user(user=user)

    def get_users(self, user_name, user_email, offset=0, limit=10) -> List[UserResponseDatasetsDTO]:
        saved_users = self.users_repository.fetch_users(user_name=user_name, user_email=user_email,
                                                        offset=offset, limit=limit)
        return saved_users

    def get_user_by_email(self, user_email: str):
        return self.users_repository.get_user_by_email(user_email)

    def get_user_by_id(self, user_id: UUID):
        return self.users_repository.get_user_by_id(user_id)

    def filter_users(self, user_filter_request, offset, limit):
        return self.users_repository.filter_users(user_filter_request, offset, limit)

    def add_user_to_project(self, project_id, user_id, user_role):
        user_orm = self.users_repository.get_user_by_id(user_id)
        project_orm = self.project_repository.get_project(project_id, session=self.session)
        project_orm.modified_at = datetime.datetime.utcnow()

        project_user_orm = self.project_user_repository \
            .save_project_user_link(user=user_orm, project=project_orm, role=user_role, session=self.session)

        self.session.commit()
        self.session.refresh(project_user_orm)
        self.session.refresh(user_orm)
        user_orm.projects = user_orm.projects
        return user_orm

    def get_project_users(self, project_id):
        project_orm = self.project_repository.get_project(project_id, session=self.session)
        users = project_orm.users
        users = [user.user for user in users]
        return users

    def get_user_projects(self, user_id):
        user_projects = self.users_repository.get_user_projects(user_id=user_id, session=self.session)
        return user_projects


