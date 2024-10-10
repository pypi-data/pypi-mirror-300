from sqlmodel import Session, select

from parsomics.entities.common.transactions import Transactions
from parsomics.entities.files.gff.entry.models import (
    GFFEntry,
    GFFEntryCreate,
    GFFEntryDemand,
    GFFEntryPublic,
)


class GFFEntryTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=GFFEntry,
            public_type=GFFEntryPublic,
            create_type=GFFEntryCreate,
            find_function=GFFEntryTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: GFFEntryDemand):
        return select(GFFEntry).where(
            GFFEntry.gene_name == demand_model.gene_name,
            GFFEntry.file_key == demand_model.file_key,
        )

    def create(self, session: Session, create_model: GFFEntryCreate) -> GFFEntryPublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: GFFEntryDemand) -> GFFEntryPublic:
        return super().demand(session, demand_model)
