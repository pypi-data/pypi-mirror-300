from typing import ClassVar

from parsomics.entities.files.validated_file import ValidatedFile


class GTDBTkValidatedFile(ValidatedFile):
    _VALID_FILE_TERMINATIONS: ClassVar[list[str]] = [
        "bac120.summary.tsv",
        "ar53.summary.tsv",
    ]
