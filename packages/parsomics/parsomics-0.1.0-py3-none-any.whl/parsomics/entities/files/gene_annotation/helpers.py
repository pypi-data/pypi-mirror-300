import logging

from sqlmodel import Session, select
from parsomics.entities.files.fasta.entry.models import FASTAEntry
from parsomics.entities.files.fasta.file.models import FASTAFile
from parsomics.entities.omics.protein.models import Protein
from parsomics.entities.workflow.assembly.models import Assembly
from parsomics.entities.workflow.run.models import Run
from parsomics.globals.database import engine


def search_protein_by_name(protein_name: str, assembly_key: int):
    statement = (
        select(Protein)
        .join(FASTAEntry)
        .join(FASTAFile)
        .join(Run)
        .join(Assembly)
        .where(FASTAEntry.sequence_name == protein_name)
        .where(Assembly.key == assembly_key)
    )

    with Session(engine) as session:
        proteins = session.exec(statement).all()
        if len(proteins) > 1:
            logging.warning(
                f"Expected only one Protein to match name {protein_name}, "
                f"but matched: {proteins}"
            )

        if not proteins:
            raise Exception(f"No Proteins were matched to name {protein_name} ")

        protein_key = proteins[0].key
        return protein_key
