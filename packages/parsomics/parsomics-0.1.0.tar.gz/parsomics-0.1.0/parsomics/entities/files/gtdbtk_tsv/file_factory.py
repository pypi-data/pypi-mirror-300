from typing import Sequence

from parsomics.entities.files.common.file_factory import FileFactory
from parsomics.entities.files.gtdbtk_tsv.validated_file import GTDBTkTsvValidatedFile


class GTDBTkTsvFileFactory(FileFactory):
    def __init__(self, path: str, dereplicated_genomes: Sequence[str]):
        return super().__init__(
            validation_class=GTDBTkTsvValidatedFile,
            path=path,
            dereplicated_genomes=dereplicated_genomes,
        )
