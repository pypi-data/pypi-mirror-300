from typing import Sequence

from parsomics.entities.files.common.file_factory import FileFactory
from parsomics.entities.files.fasta.validated_file import FASTAValidatedFile


class FASTAFileFactory(FileFactory):
    def __init__(self, path: str, dereplicated_genomes: Sequence[str] | None = None):
        return super().__init__(
            validation_class=FASTAValidatedFile,
            path=path,
            dereplicated_genomes=dereplicated_genomes,
        )
