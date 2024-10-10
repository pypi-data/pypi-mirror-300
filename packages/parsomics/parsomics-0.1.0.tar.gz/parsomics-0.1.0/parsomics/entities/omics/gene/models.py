from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics.entities.files.fasta.entry.models import FASTAEntry
    from parsomics.entities.omics.contig.models import Contig
    from parsomics.entities.omics.fragment.models import Fragment
    from parsomics.entities.files.gene_annotation.entry.models import (
        GeneAnnotationEntry,
    )


class GeneBase(SQLModel):
    fasta_entry_key: int = Field(default=None, foreign_key="fastaentry.key")
    contig_key: int = Field(default=None, foreign_key="contig.key")


class Gene(GeneBase, table=True):
    __table_args__ = (UniqueConstraint("fasta_entry_key"),)

    key: int | None = Field(default=None, primary_key=True)

    contig: "Contig" = Relationship(back_populates="genes")
    fragments: list["Fragment"] = Relationship(back_populates="gene")

    fasta_entry: "FASTAEntry" = Relationship(
        sa_relationship_kwargs={"uselist": False},
        back_populates="gene",
    )
    gene_annotation_entries: list["GeneAnnotationEntry"] = Relationship(
        back_populates="gene"
    )


class GenePublic(GeneBase):
    key: int


class GeneCreate(GeneBase):
    pass


class GeneDemand(GeneCreate):
    pass
