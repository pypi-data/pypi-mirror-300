from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics.entities.workflow.common.progress import Progress
from parsomics.entities.workflow.common.timestamp import Timestamp

if TYPE_CHECKING:
    from parsomics.entities.workflow.assembly.models import Assembly


class ProjectBase(SQLModel, Progress):
    name: str


class Project(ProjectBase, Timestamp, table=True):
    __table_args__ = (UniqueConstraint("name"),)

    key: int | None = Field(default=None, primary_key=True)

    assemblies: list["Assembly"] = Relationship(back_populates="project")


class ProjectPublic(ProjectBase):
    key: int


class ProjectCreate(ProjectBase):
    pass


class ProjectDemand(ProjectCreate):
    pass
