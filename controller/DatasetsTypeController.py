from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends, Body
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from auth.inject_user import get_current_user
from auth.jwt_bearer import JwtBearer
from dao.DatasetType import DatasetType
from dao.Users import Users
from dto.DTO import DatasetTypeDTO, DatasetTypeFilterDTO
from service.DatasetTypeService import DatasetTypeService

router = APIRouter(prefix="/api/v1/dataset-type", tags=["Dataset Type"])


@router.post("/", status_code=HTTP_201_CREATED, dependencies=[Depends(JwtBearer())])
def add_dataset_type(dataset_type: DatasetTypeDTO,
                     dataset_type_service: DatasetTypeService = Depends(),
                     current_user: Users = Depends(get_current_user)):
    return dataset_type_service.create_new_dataset_type(dataset_type)


@router.post("/filter", status_code=HTTP_200_OK, dependencies=[Depends(JwtBearer())],
             response_model=List[DatasetType])
def filter_dataset_type(dataset_type: DatasetTypeFilterDTO = Body(), offset: int = 0, limit: int = 10,
                        dataset_type_service: DatasetTypeService = Depends()):
    return dataset_type_service.filter_dataset_type(dataset_type, offset=offset, limit=limit)


@router.get("/", status_code=HTTP_200_OK, dependencies=[Depends(JwtBearer())],
            response_model=List[DatasetType])
def get_datasets(dataset_type_name: str | None = None, offset: int = 0, limit: int = 10,
                 dataset_type_service: DatasetTypeService = Depends()):
    return dataset_type_service.filter_dataset_type_by_name(dataset_type_name, offset=offset, limit=limit)


@router.get("/{dataset_type_id}", status_code=HTTP_200_OK, dependencies=[Depends(JwtBearer())],
            response_model=DatasetType)
def get_dataset_by_id(dataset_type_id: UUID | None = None, dataset_type_service: DatasetTypeService = Depends()):
    return dataset_type_service.get_dataset_by_id(dataset_type_id)