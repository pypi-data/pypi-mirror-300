from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics.entities.files.gtdbtk_tsv.entry.models import GTDBTkTsvEntry
from parsomics.entities.files.gtdbtk_tsv.validated_file import GTDBTkTsvValidatedFile

if TYPE_CHECKING:
    from parsomics.entities.workflow.run.models import Run

# File -----------------------------------------------------------------------


class GTDBTkTsvFileBase(SQLModel):
    path: str
    run_key: int = Field(default=None, foreign_key="run.key")

    @field_validator("path")
    def path_must_be_validated(cls, path: str) -> str:
        _ = GTDBTkTsvValidatedFile(path=path)
        return path


class GTDBTkTsvFile(GTDBTkTsvFileBase, table=True):
    __table_args__ = (UniqueConstraint("path"),)

    key: int | None = Field(default=None, primary_key=True)

    entries: list["GTDBTkTsvEntry"] = Relationship(back_populates="file")
    run: "Run" = Relationship(back_populates="gtdbtk_tsv_files")


class GTDBTkTsvFilePublic(GTDBTkTsvFileBase):
    key: int


class GTDBTkTsvFileCreate(GTDBTkTsvFileBase):
    pass


class GTDBTkTsvFileDemand(GTDBTkTsvFileCreate):
    pass
