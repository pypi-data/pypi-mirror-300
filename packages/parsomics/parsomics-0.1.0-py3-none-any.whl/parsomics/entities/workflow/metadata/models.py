from sqlmodel import Field, SQLModel

from parsomics.entities.workflow.common.progress import Progress
from parsomics.entities.workflow.common.timestamp import Timestamp


class MetadataBase(SQLModel, Progress):
    pass


class Metadata(MetadataBase, Timestamp, table=True):
    key: int | None = Field(default=None, primary_key=True)


class MetadataPublic(MetadataBase):
    key: int


class MetadataCreate(MetadataBase):
    pass


class MetadataDemand(MetadataBase):
    pass
