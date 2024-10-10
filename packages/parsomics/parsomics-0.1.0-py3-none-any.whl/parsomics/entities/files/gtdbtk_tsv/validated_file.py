from typing import ClassVar

from parsomics.entities.files.common.validated_file import ValidatedFile


class GTDBTkTsvValidatedFile(ValidatedFile):
    _VALID_FILE_TERMINATIONS: ClassVar[list[str]] = [
        "bac120.summary.tsv",
        "ar53.summary.tsv",
    ]
