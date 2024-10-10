from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics.entities.files.gtdbtk_tsv.file.models import GTDBTkTsvFile
    from parsomics.entities.omics.genome.models import Genome


class GTDBTkTsvEntryBase(SQLModel):
    # Source: https://en.wikipedia.org/wiki/GTDBTkTsv_format#Overview
    reference: str | None
    radius: float | None
    ani: float | None
    af: float | None

    classification_method: str
    note: str
    red_value: float | None
    warnings: str | None

    domain: str
    phylum: str
    klass: str  # NOTE: cannot be "class" because it is a reserved word
    order: str
    family: str
    genus: str
    species: str
    taxonomic_novelty: bool

    genome_key: int = Field(default=None, foreign_key="genome.key")
    file_key: int = Field(default=None, foreign_key="gtdbtktsvfile.key")


class GTDBTkTsvEntry(GTDBTkTsvEntryBase, table=True):
    __table_args__ = (UniqueConstraint("file_key", "genome_key"),)

    key: int | None = Field(default=None, primary_key=True)

    file: "GTDBTkTsvFile" = Relationship(back_populates="entries")
    genome: "Genome" = Relationship(back_populates="gtdbtk_tsv_entry")


class GTDBTkTsvEntryPublic(GTDBTkTsvEntryBase):
    key: int


class GTDBTkTsvEntryCreate(GTDBTkTsvEntryBase):
    pass


class GTDBTkTsvEntryDemand(GTDBTkTsvEntryCreate):
    pass
