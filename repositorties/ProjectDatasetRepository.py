from uuid import UUID

from sqlmodel import Session

from dao.ProjectDataset import ProjectDataset


class ProjectDatasetRepository:
    def save_project_dataset_link(self, dataset, project, project_dataset_state, session: Session):
        entity = ProjectDataset(project=project, dataset=dataset, project_dataset_state=project_dataset_state)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    def get_project_dataset_by_id(self, session: Session, project_id: UUID, dataset_id: UUID):
        entity = session.get(ProjectDataset, (project_id, dataset_id))
        return entity
