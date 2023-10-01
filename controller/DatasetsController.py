from uuid import UUID
from typing import List

from fastapi import APIRouter, Body
from fastapi import Depends
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED

from auth.jwt_bearer import JwtBearer
from dto.DTO import ProjectDatasetInput, DatasetsOutput, DatasetsWithDatasetTypeDTO, DatasetUpdateDTO
from service.DatasetService import DatasetService

router = APIRouter(prefix="/api/v1/datasets", tags=["Datasets"])


@router.post("/", status_code=HTTP_201_CREATED, dependencies=[Depends(JwtBearer())],
             response_model=DatasetsOutput)
def add_dataset(dataset: ProjectDatasetInput = Body(), dataset_service: DatasetService = Depends()):
    saved_dataset = dataset_service.create_new_dataset(project_id=dataset.dataset.project_id, dataset=dataset)
    return saved_dataset


@router.get("/", status_code=HTTP_200_OK, response_model=List[DatasetsWithDatasetTypeDTO],
            dependencies=[Depends(JwtBearer())])
def find_dataset(project_id: UUID | None = None,
                 dataset_type_id: UUID | None = None,
                 dataset_name: str | None = None,
                 dataset_state_query: str | None = None,
                 dataset_service: DatasetService = Depends()):
    filtered_datasets = dataset_service.find_dataset(project_id=project_id, dataset_type_id=dataset_type_id,
                                                     dataset_name=dataset_name, dataset_state_query=dataset_state_query)
    return filtered_datasets


@router.get("/{dataset_id}", status_code=HTTP_200_OK, response_model=DatasetsWithDatasetTypeDTO,
            dependencies=[Depends(JwtBearer())])
def find_dataset(dataset_id: UUID | None = None,
                 dataset_service: DatasetService = Depends()):
    dataset = dataset_service.get_dataset_by_id(dataset_id=dataset_id)
    return dataset


@router.delete("/{dataset_id}", status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(JwtBearer())])
def delete_dataset(dataset_id: UUID | None = None,
                   dataset_service: DatasetService = Depends()):
    dataset_service.delete_dataset(dataset_id)


@router.put("/{dataset_id}", status_code=HTTP_202_ACCEPTED, response_model=DatasetsWithDatasetTypeDTO,
            dependencies=[Depends(JwtBearer())])
def update_dataset(dataset_id: UUID, dataset_dto: DatasetUpdateDTO = Body(),
                        dataset_service: DatasetService = Depends()):
    updated_dataset = dataset_service.update_dataset(dataset_id, dataset_dto)
    return updated_dataset


@router.get("/parent/{parent_dataset_id}", status_code=HTTP_200_OK, response_model=List[DatasetsWithDatasetTypeDTO],
            dependencies=[Depends(JwtBearer())])
def find_dataset(parent_dataset_id: UUID | None = None,
                 dataset_service: DatasetService = Depends()):
    dataset = dataset_service.get_dataset_by_parent_id(dataset_id=parent_dataset_id)
    return dataset
