from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from parsomics.entities.omics.fragment.models import Fragment
    from parsomics.entities.omics.protein.models import Protein


class FragmentProteinLink(SQLModel, table=True):
    fragment_key: int | None = Field(
        default=None,
        foreign_key="fragment.key",
        primary_key=True,
    )
    protein_key: int | None = Field(
        default=None,
        foreign_key="protein.key",
        primary_key=True,
    )

    protein: "Protein" = Relationship(sa_relationship_kwargs={"viewonly": True})
    fragment: "Fragment" = Relationship(sa_relationship_kwargs={"viewonly": True})
