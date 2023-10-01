from sqlmodel import Session

from dao.ProjectsUsers import ProjectsUsers


class ProjectUserRepository:

    def save_project_user_link(self, user, project, role, session: Session):
        entity = ProjectsUsers(project=project, user=user, role=role)
        session.add(entity)
        return entity
