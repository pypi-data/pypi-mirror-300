from typing import TYPE_CHECKING, Union

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics.entities.omics.fragment_protein_link.models import FragmentProteinLink

if TYPE_CHECKING:
    from parsomics.entities.files.fasta.entry.models import FASTAEntry
    from parsomics.entities.omics.fragment.models import Fragment
    from parsomics.entities.files.protein_annotation.entry.models import (
        ProteinAnnotationEntry,
    )


class ProteinBase(SQLModel):
    fasta_entry_key: int | None = Field(default=None, foreign_key="fastaentry.key")


class Protein(ProteinBase, table=True):
    __table_args__ = (UniqueConstraint("fasta_entry_key"),)

    key: int | None = Field(default=None, primary_key=True)

    fragments: list["Fragment"] = Relationship(
        back_populates="proteins", link_model=FragmentProteinLink
    )
    fasta_entry: Union["FASTAEntry", None] = Relationship(
        sa_relationship_kwargs={"uselist": False},
        back_populates="protein",
    )
    protein_annotation_entries: list["ProteinAnnotationEntry"] = Relationship(
        back_populates="protein"
    )


class ProteinPublic(ProteinBase):
    key: int


class ProteinCreate(ProteinBase):
    pass
