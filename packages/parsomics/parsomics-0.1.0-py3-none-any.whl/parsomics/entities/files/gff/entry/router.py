from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics.entities.common.routing_helpers import RoutingHelpers
from parsomics.entities.files.gff.entry.models import (
    GFFEntry,
    GFFEntryCreate,
    GFFEntryDemand,
    GFFEntryPublic,
)
from parsomics.entities.files.gff.entry.transactions import GFFEntryTransactions
from parsomics.globals.database import get_session

_routing_helpers = RoutingHelpers(
    table_type=GFFEntry,
    transactions=GFFEntryTransactions(),
)
router = APIRouter(
    prefix="/entry",
    tags=["files/gff/entry"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/", response_model=list[GFFEntryPublic])
def read_entries(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)


@router.post("/create", response_model=GFFEntryPublic)
def create_entry(
    *,
    session: Session = Depends(get_session),
    create_model: GFFEntryCreate,
):
    return _routing_helpers.create(session, create_model)


@router.post("/demand", response_model=GFFEntryPublic)
def demand_entry(
    *,
    session: Session = Depends(get_session),
    demand_model: GFFEntryDemand,
):
    return _routing_helpers.demand(session, demand_model)
