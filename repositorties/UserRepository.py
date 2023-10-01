from fastapi import Depends
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select, or_, any_, col, and_

from dao.Users import Users
from db import get_session
from dto.DTO import UsersDTO, UsersResponseDTO, UserFilterRequest


class UserRepository:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_user_by_email(self, user_email):
        user = self.session.execute(select(Users).where(Users.email == user_email)).one()
        return user

    def add_user(self, user: UsersDTO) -> UsersResponseDTO:
        user_orm = Users.from_orm(user)
        self.session.add(user_orm)
        self.session.commit()
        self.session.refresh(user_orm)
        return user_orm

    def fetch_users(self, user_name="", user_email="", offset=-1, limit=-1):

        user_name_query = f'%{user_name or ""}%'
        user_email_query = f'%{user_email or ""}%'
        query = select(Users).where(and_(
            col(Users.first_name).ilike(user_name_query), col(Users.email).ilike(user_email_query)))

        if offset >= 0 and limit >= 0:
            query = query.offset(offset).limit(limit)
        query = query.options(joinedload(Users.projects))
        res = self.session.execute(query).unique().scalars().all()
        return res

    def get_user_by_id(self, user_id):
        return self.session.get(Users, user_id)

    def filter_users(self, user_filter_request: UserFilterRequest, offset=-1, limit=-1):
        query = select(Users).where(or_(col(Users.email).in_(user_filter_request.emails),
                                        col(Users.first_name).in_(user_filter_request.first_names)))

        if offset >= 0 and limit >= 0:
            query = query.offset(offset).limit(limit)

        res = self.session.execute(query).unique().scalars().all()
        return res

    def get_user_projects(self, user_id, session: Session):
        user_orm = session.get(Users, user_id)
        user_orm_projects = user_orm.projects
        projects = [uop.project for uop in user_orm_projects]
        return projects
