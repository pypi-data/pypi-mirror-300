from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics.entities.common.routing_helpers import RoutingHelpers
from parsomics.entities.files.drep.entry.models import (
    DrepEntry,
    DrepEntryCreate,
    DrepEntryDemand,
    DrepEntryPublic,
)
from parsomics.entities.files.drep.entry.transactions import DrepEntryTransactions
from parsomics.globals.database import get_session

_routing_helpers = RoutingHelpers(
    table_type=DrepEntry,
    transactions=DrepEntryTransactions(),
)
router = APIRouter(
    prefix="/entry",
    tags=["files/drep/entry"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/", response_model=list[DrepEntryPublic])
def read_entries(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)


@router.post("/create", response_model=DrepEntryPublic)
def create_entry(
    *,
    session: Session = Depends(get_session),
    create_model: DrepEntryCreate,
):
    return _routing_helpers.create(session, create_model)


@router.post("/demand", response_model=DrepEntryPublic)
def demand_entry(
    *,
    session: Session = Depends(get_session),
    demand_model: DrepEntryDemand,
):
    return _routing_helpers.demand(session, demand_model)
