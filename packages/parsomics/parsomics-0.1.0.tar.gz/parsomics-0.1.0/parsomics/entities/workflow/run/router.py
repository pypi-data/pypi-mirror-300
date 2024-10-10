from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics.entities.common.routing_helpers import RoutingHelpers
from parsomics.entities.workflow.run.models import Run, RunCreate, RunDemand, RunPublic
from parsomics.entities.workflow.run.transactions import RunTransactions
from parsomics.globals.database import get_session

_routing_helpers = RoutingHelpers(
    table_type=Run,
    transactions=RunTransactions(),
)
router = APIRouter(
    prefix="/run",
    tags=["workflow/run"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/", response_model=list[RunPublic])
def read_runs(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)


@router.post("/create", response_model=RunPublic)
def create_run(
    *,
    session: Session = Depends(get_session),
    create_model: RunCreate,
):
    return _routing_helpers.create(session, create_model)


@router.post("/demand", response_model=RunPublic)
def demand_run(
    *,
    session: Session = Depends(get_session),
    demand_model: RunDemand,
):
    return _routing_helpers.demand(session, demand_model)
