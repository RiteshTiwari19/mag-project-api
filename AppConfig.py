import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_409_CONFLICT
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer

from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from sqlmodel import SQLModel
from sqlalchemy.exc import IntegrityError

from db import engine
from controller import ProjectsController, DatasetsTypeController, UserController, DatasetsController
from dao import Dataset, DatasetType, ProjectDataset, Projects, ProjectsUsers, \
    Users

origins = [
    "http://localhost:8050",
    "http://localhost:8080"
]

app = FastAPI(
    title="Magnetometer API",
    description="Backend API for the UCC Magnetometer Application",
    version="0.0.1",
    contact={
        "name": "Ritesh Tiwari",
        "email": "riteshtiwari@hotmail.co.uk",
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(ProjectsController.router)
app.include_router(DatasetsTypeController.router)
app.include_router(UserController.router)
app.include_router(DatasetsController.router)


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    if type(exc.orig) == UniqueViolation:
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"message": "Unique Key Violation when trying to create resource"},
        )
    elif type(exc.orig) == ForeignKeyViolation:
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"message": "Foreign Key Violation when trying to create resource! Make sure the resources exist"},
        )


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run("AppConfig:app", reload=True)
