from typing import TYPE_CHECKING, Callable

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics.entities.files.common.validated_file import ValidatedFileWithGenome

if TYPE_CHECKING:
    from parsomics.entities.files.protein_annotation.entry.models import (
        ProteinAnnotationEntry,
    )
    from parsomics.entities.omics.genome.models import Genome
    from parsomics.entities.workflow.run.models import Run


class ProteinAnnotationFileBase(SQLModel):
    path: str
    run_key: int = Field(default=None, foreign_key="run.key")
    genome_key: int = Field(default=None, foreign_key="genome.key")


class ProteinAnnotationFile(ProteinAnnotationFileBase, table=True):
    __table_args__ = (UniqueConstraint("path"),)

    key: int | None = Field(default=None, primary_key=True)

    entries: list["ProteinAnnotationEntry"] = Relationship(back_populates="file")
    genome: "Genome" = Relationship(back_populates="protein_annotation_files")
    run: "Run" = Relationship(back_populates="protein_annotation_files")


class ProteinAnnotationFilePublic(ProteinAnnotationFileBase):
    key: int


class ProteinAnnotationFileCreate(ProteinAnnotationFileBase):
    pass


class ProteinAnnotationFileDemand(ProteinAnnotationFileCreate):
    pass
