from typing import ClassVar

from parsomics.entities.files.common.validated_directory import ValidatedDirectory


class DrepValidatedDirectory(ValidatedDirectory):
    _MUST_CONTAIN_FILES: ClassVar[list[str]] = [
        "Wdb.csv",
        "Cdb.csv",
    ]
