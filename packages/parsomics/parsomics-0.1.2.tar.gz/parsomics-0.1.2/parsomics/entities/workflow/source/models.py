from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics.entities.workflow.tool.models import Tool

if TYPE_CHECKING:
    from parsomics.entities.files.fasta.entry.models import FASTAEntry
    from parsomics.entities.files.gene_annotation.entry.models import (
        GeneAnnotationEntry,
    )
    from parsomics.entities.files.gff.entry.models import GFFEntry
    from parsomics.entities.files.protein_annotation.entry.models import (
        ProteinAnnotationEntry,
    )


class SourceBase(SQLModel):
    name: str
    version: str | None = None
    reliability: float | None = Field(default=None, ge=0.0, le=1.0)

    tool_key: int = Field(default=None, foreign_key="tool.key")


class Source(SourceBase, table=True):
    __table_args__ = (UniqueConstraint("name", "version"),)

    key: int | None = Field(default=None, primary_key=True)

    tool: Tool = Relationship(back_populates="sources")

    fasta_entries: list["FASTAEntry"] = Relationship(back_populates="source")
    gff_entries: list["GFFEntry"] = Relationship(back_populates="source")
    protein_annotation_entries: list["ProteinAnnotationEntry"] = Relationship(
        back_populates="source"
    )
    gene_annotation_entries: list["GeneAnnotationEntry"] = Relationship(
        back_populates="source"
    )


class SourcePublic(SourceBase):
    key: int


class SourceCreate(SourceBase):
    pass


class SourceDemand(SourceCreate):
    pass
