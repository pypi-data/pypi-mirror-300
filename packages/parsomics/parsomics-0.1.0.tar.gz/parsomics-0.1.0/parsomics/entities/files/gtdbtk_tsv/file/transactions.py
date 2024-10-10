from sqlmodel import Session, select

from parsomics.entities.common.transactions import Transactions
from parsomics.entities.files.gtdbtk_tsv.file.models import (
    GTDBTkTsvFile,
    GTDBTkTsvFileCreate,
    GTDBTkTsvFileDemand,
    GTDBTkTsvFilePublic,
)


class GTDBTkTsvFileTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=GTDBTkTsvFile,
            public_type=GTDBTkTsvFilePublic,
            create_type=GTDBTkTsvFileCreate,
            find_function=GTDBTkTsvFileTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: GTDBTkTsvFileDemand):
        return select(GTDBTkTsvFile).where(
            GTDBTkTsvFile.path == demand_model.path,
        )

    def create(
        self, session: Session, create_model: GTDBTkTsvFileCreate
    ) -> GTDBTkTsvFilePublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: GTDBTkTsvFileDemand
    ) -> GTDBTkTsvFilePublic:
        return super().demand(session, demand_model)
