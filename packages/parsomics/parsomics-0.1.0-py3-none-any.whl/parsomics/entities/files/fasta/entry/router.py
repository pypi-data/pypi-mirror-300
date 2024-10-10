from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics.entities.common.routing_helpers import RoutingHelpers
from parsomics.entities.files.fasta.entry.models import (
    FASTAEntry,
    FASTAEntryCreate,
    FASTAEntryDemand,
    FASTAEntryPublic,
)
from parsomics.entities.files.fasta.entry.transactions import FASTAEntryTransactions
from parsomics.globals.database import get_session

_routing_helpers = RoutingHelpers(
    table_type=FASTAEntry,
    transactions=FASTAEntryTransactions(),
)
router = APIRouter(
    prefix="/entry",
    tags=["files/fasta/entry"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/", response_model=list[FASTAEntryPublic])
def read_entries(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)


@router.post("/create", response_model=FASTAEntryPublic)
def create_entry(
    *,
    session: Session = Depends(get_session),
    create_model: FASTAEntryCreate,
):
    return _routing_helpers.create(session, create_model)


@router.post("/demand", response_model=FASTAEntryPublic)
def demand_entry(
    *,
    session: Session = Depends(get_session),
    demand_model: FASTAEntryDemand,
):
    return _routing_helpers.demand(session, demand_model)
