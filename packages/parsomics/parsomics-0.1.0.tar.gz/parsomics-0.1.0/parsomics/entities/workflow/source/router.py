from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics.entities.common.routing_helpers import RoutingHelpers
from parsomics.entities.workflow.source.models import (
    Source,
    SourceCreate,
    SourceDemand,
    SourcePublic,
)
from parsomics.entities.workflow.source.transactions import SourceTransactions
from parsomics.globals.database import get_session

_routing_helpers = RoutingHelpers(
    table_type=Source,
    transactions=SourceTransactions(),
)
router = APIRouter(
    prefix="/source",
    tags=["workflow/source"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/", response_model=list[SourcePublic])
def read_sources(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)


@router.post("/create", response_model=SourcePublic)
def create_source(
    *,
    session: Session = Depends(get_session),
    create_model: SourceCreate,
):
    return _routing_helpers.create(session, create_model)


@router.post("/demand", response_model=SourcePublic)
def demand_source(
    *,
    session: Session = Depends(get_session),
    demand_model: SourceDemand,
):
    return _routing_helpers.demand(session, demand_model)
