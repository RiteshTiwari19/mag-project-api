from typing import List
from uuid import UUID

from fastapi import APIRouter, Body
from fastapi import Depends
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from auth.jwt_bearer import JwtBearer
from dto.DTO import UsersDTO, UsersResponseDTO, UserResponseDatasetsDTO, UserFilterRequest, ProjectsOutput
from service.UserService import UserService

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/", status_code=HTTP_201_CREATED, dependencies=[Depends(JwtBearer())])
def create_new_user(user: UsersDTO, user_service: UserService = Depends()) -> UsersResponseDTO:
    saved_user = user_service.save_user(user)
    return saved_user


@router.post("/filter", status_code=HTTP_200_OK, dependencies=[Depends(JwtBearer())],
             response_model=List[UserResponseDatasetsDTO])
def filter_user(user_filter_request: UserFilterRequest = Body(), offset: int = 0, limit: int = 10, user_service: UserService = Depends()) -> UsersResponseDTO:
    users = user_service.filter_users(user_filter_request, offset=offset, limit=limit)
    return users


@router.get("/", status_code=HTTP_200_OK, dependencies=[Depends(JwtBearer())],
            response_model=List[UserResponseDatasetsDTO])
def get_users(user_name: str | None = None, user_email: str | None = None,
              offset: int = 0, limit: int = 10, user_service: UserService = Depends()):
    saved_users = user_service.get_users(user_name=user_name, user_email=user_email, offset=offset, limit=limit)
    return saved_users


@router.get("/{user_id}", status_code=HTTP_200_OK, dependencies=[Depends(JwtBearer())], response_model=UserResponseDatasetsDTO)
def get_user_by_id(user_id: UUID, user_service: UserService = Depends()):
    return user_service.get_user_by_id(user_id)


@router.get("/{user_id}/projects", status_code=HTTP_200_OK, dependencies=[Depends(JwtBearer())],
            response_model=List[ProjectsOutput])
def get_user_projects(user_id: UUID, user_service: UserService = Depends()):
    return user_service.get_user_projects(user_id)

