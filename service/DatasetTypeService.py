from fastapi import Depends
from sqlmodel import Session

from db import get_session
from dto.DTO import DatasetTypeFilterDTO
from repositorties.DatasetTypeRepository import DatasetTypeRepository


class DatasetTypeService:

    def __init__(self, dataset_type_repository: DatasetTypeRepository = Depends(),
                 session: Session = Depends(get_session)):
        self.dataset_type_repository = dataset_type_repository
        self.session = session

    def create_new_dataset_type(self, dataset_type):
        return self.dataset_type_repository.create_new_dataset_type(dataset_type, self.session)

    def filter_dataset_type(self, dataset_type: DatasetTypeFilterDTO, offset: int = -1, limit: int = -1):
        return self.dataset_type_repository.filter_dataset_type(dataset_type=dataset_type, offset=offset,
                                                                limit=limit, session=self.session)

    def filter_dataset_type_by_name(self, dataset_type_name: str, offset: int = -1, limit: int = -1):
        return self.dataset_type_repository.find_dataset_type_by_name(dataset_type_name=dataset_type_name,
                                                                      offset=offset,
                                                                      limit=limit, session=self.session)

    def get_dataset_by_id(self, dataset_type_id):
        return self.dataset_type_repository.get_dataset_by_id(dataset_type_id=dataset_type_id, session=self.session)
