import datetime
from uuid import UUID
from typing import List, Optional
import numpy as np

from fastapi import Depends
from sqlmodel import Session, select, and_, col
from sqlalchemy.orm import joinedload

from dao.Dataset import Dataset
from dto.DTO import ProjectDatasetInput
from repositorties.DatasetTypeRepository import DatasetTypeRepository


class DatasetRepository:

    def __init__(self, dataset_type_repository: DatasetTypeRepository = Depends()):
        self.dataset_type_repository = dataset_type_repository

    def add_new_dataset(self, dataset: ProjectDatasetInput, session: Session):
        dataset_type_orm = self.dataset_type_repository.get_dataset_type_by_id(dataset.dataset.dataset_type_id, session)

        if not dataset.dataset.tags:
            dataset.dataset.tags = {}

        dataset.dataset.tags['created_at'] = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
        dataset.dataset.tags['modified_at'] = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")

        dataset_orm = Dataset.from_orm(dataset.dataset, update={'dataset_type': dataset_type_orm})
        session.add(dataset_orm)
        return dataset_orm

    def get_dataset_by_id(self, dataset_id: UUID, session: Session):
        return session.get(Dataset, dataset_id)

    def find_datasetby_dataset_name(self, dataset_name: str, project_id: UUID, dataset_type_id: UUID | None,
                                    dataset_states: Optional[List],
                                    session: Session):
        dataset_name_query = f'%{dataset_name or ""}%'

        where_clause = col(Dataset.name).ilike(dataset_name_query) if not dataset_type_id \
            else and_(Dataset.dataset_type_id == dataset_type_id, col(Dataset.name).ilike(dataset_name_query))

        query = select(Dataset).where(where_clause)\
            .options(joinedload(Dataset.projects)).options(joinedload(Dataset.dataset_type))
        res: List[Dataset] = session.execute(query).unique().scalars().all()

        if project_id:
            res = [re for re in res if any(str(project.project.id) == str(project_id) for project in re.projects)]

        if dataset_states:
            res = [re for re in res if 'state' in re.tags and re.tags['state'] in dataset_states]

        return res

    def delete_dataset(self, dataset_id, session: Session):
        dataset_to_delete = self.get_dataset_by_id(dataset_id=dataset_id, session=session)
        session.delete(dataset_to_delete)
        session.commit()

    def get_all_datasets(self, session, limit=-1, offset=-1):
        query = select(Dataset).options(joinedload(Dataset.projects)).options(joinedload(Dataset.dataset_type))

        if offset >= 0 and limit >= 0:
            query.offset(offset).limit(limit)

        datasets = session.execute(query).unique().scalars().all()

        return datasets

    def get_dataset_by_parent_id(self, dataset_id, session: Session):
        query = select(Dataset).where(Dataset.parent_dataset_id == dataset_id)\
            .options(joinedload(Dataset.projects)).options(joinedload(Dataset.dataset_type))
        datasets = session.execute(query).unique().scalars().all()
        return datasets

