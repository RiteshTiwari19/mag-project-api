import datetime
from copy import deepcopy
from uuid import UUID

from fastapi import Depends
from sqlmodel import Session, select

from dao.Dataset import Dataset
from db import get_session
from dto.DTO import ProjectDatasetInput, DatasetUpdateDTO
from repositorties.DatasetRepository import DatasetRepository
from repositorties.ProjectDatasetRepository import ProjectDatasetRepository
from repositorties.ProjectsRepository import ProjectsRepository


class DatasetService:
    def __init__(self, dataset_repository: DatasetRepository = Depends(),
                 project_dataset_repository: ProjectDatasetRepository = Depends(),
                 project_repository: ProjectsRepository = Depends(),
                 session: Session = Depends(get_session)):
        self.dataset_repository = dataset_repository
        self.project_dataset_repository = project_dataset_repository
        self.project_repository = project_repository
        self.session = session

    def create_new_dataset(self, project_id: UUID, dataset: ProjectDatasetInput = None,
                           dataset_id: UUID = None, project_dataset_state: str = None):
        if not dataset_id:
            dataset_orm = self.dataset_repository.add_new_dataset(dataset=dataset, session=self.session)
        else:
            dataset_orm = self.dataset_repository.get_dataset_by_id(dataset_id=dataset_id, session=self.session)

        if project_id:
            project_orm = self.project_repository.get_project(project_id, session=self.session)
            project_orm.modified_at = datetime.datetime.utcnow()

            dataset_link_orm = self.project_dataset_repository.save_project_dataset_link(
                project=project_orm,
                dataset=dataset_orm,
                project_dataset_state=dataset.project_dataset_state if dataset else project_dataset_state,
                session=self.session)

            self.session.add(dataset_link_orm)

        self.session.commit()
        self.session.refresh(dataset_orm)
        dataset_orm.projects = dataset_orm.projects
        return dataset_orm

    def find_dataset(self, project_id: UUID | None = None, dataset_type_id: UUID | None = None,
                     dataset_name: str | None = None, dataset_state_query: str | None = None):

        dataset_states = []
        if dataset_state_query:
            dataset_states = dataset_state_query.split(';')

        if not project_id and not dataset_name and not dataset_type_id and not dataset_state_query:
            datasets = self.dataset_repository.get_all_datasets(session=self.session, offset=0, limit=20)

        elif dataset_name or dataset_type_id or dataset_state_query:
            datasets = self.dataset_repository.find_datasetby_dataset_name(dataset_name=dataset_name,
                                                                           session=self.session,
                                                                           dataset_type_id=dataset_type_id,
                                                                           project_id=project_id,
                                                                           dataset_states=dataset_states)

        else:
            datasets = self.project_repository.get_project(project_id=project_id, session=self.session)
            datasets = [ds.dataset for ds in datasets.datasets]

        return datasets

    def get_dataset_by_id(self, dataset_id):
        return self.dataset_repository.get_dataset_by_id(dataset_id, session=self.session)

    def delete_dataset(self, dataset_id):
        self.dataset_repository.delete_dataset(dataset_id=dataset_id, session=self.session)

    def update_dataset(self, dataset_id, dataset_dto: DatasetUpdateDTO):
        dataset_to_update = self.session.get(Dataset, dataset_id)

        if dataset_dto.tags:
            existing_tags = deepcopy(dataset_to_update.tags or {})
            existing_tags.update(dataset_dto.tags)
            dataset_to_update.tags = existing_tags

        if dataset_dto.name:
            dataset_to_update.name = dataset_dto.name

        if dataset_dto.path:
            dataset_to_update.path = dataset_dto.path

        dataset_to_update.modified_at = datetime.datetime.utcnow()
        dataset_to_update.tags['modified_at'] = dataset_to_update.modified_at.strftime("%m/%d/%Y, %H:%M:%S")

        self.session.commit()
        self.session.refresh(dataset_to_update)

        dataset_to_update.projects = dataset_to_update.projects

        return dataset_to_update

    def get_dataset_by_parent_id(self, dataset_id):
        return self.dataset_repository.get_dataset_by_parent_id(dataset_id, session=self.session)

