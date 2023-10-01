from sqlmodel import Session, select
from sqlmodel import Session, select,  or_, any_, col
import sqlalchemy

from dao.DatasetType import DatasetType
from dto.DTO import DatasetTypeFilterDTO


class DatasetTypeRepository:
    def create_new_dataset_type(self, dataset_type, session: Session):
        dataset_type_orm = DatasetType.from_orm(dataset_type)
        session.add(dataset_type_orm)
        session.commit()
        session.refresh(dataset_type_orm)
        return dataset_type_orm

    def get_dataset_type_by_id(self, dataset_type_id, session: Session):
        dataset_type = session.get(DatasetType, dataset_type_id)
        return dataset_type

    def filter_dataset_type(self, dataset_type: DatasetTypeFilterDTO, offset, limit, session):
        query = select(DatasetType).where(col(DatasetType.name).in_(dataset_type.names))

        if offset > 0 and limit > 0:
            query = query.offset(offset).limit(limit)

        res = session.execute(query).unique().scalars().all()
        return res

    def find_dataset_type_by_name(self, dataset_type_name: str, session: Session, offset=-1, limit=-1):
        if dataset_type_name:
            query = select(DatasetType).where(col(DatasetType.name).ilike(f'%{dataset_type_name}%'))
        else:
            query = select(DatasetType).where(col(DatasetType.name).ilike(f'%%'))

        if offset >= 0 and limit >= 0:
            query = query.offset(offset).limit(limit)

        res = session.execute(query).unique().scalars().all()
        return res

    def get_dataset_by_id(self, dataset_type_id, session: Session):
        return session.get(DatasetType, dataset_type_id)
