from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics.entities.common.routing_helpers import RoutingHelpers
from parsomics.entities.files.drep.directory.models import (
    DrepDirectory,
    DrepDirectoryCreate,
    DrepDirectoryDemand,
    DrepDirectoryPublic,
)
from parsomics.entities.files.drep.directory.transactions import (
    DrepDirectoryTransactions,
)
from parsomics.globals.database import get_session

_routing_helpers = RoutingHelpers(
    table_type=DrepDirectory,
    transactions=DrepDirectoryTransactions(),
)
router = APIRouter(
    prefix="/directory",
    tags=["files/drep/directory"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/", response_model=list[DrepDirectoryPublic])
def read_directories(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)


@router.post("/create", response_model=DrepDirectoryPublic)
def create_directory(
    *,
    session: Session = Depends(get_session),
    create_model: DrepDirectoryCreate,
):
    return _routing_helpers.create(session, create_model)


@router.post("/demand", response_model=DrepDirectoryPublic)
def demand_directory(
    *,
    session: Session = Depends(get_session),
    demand_model: DrepDirectoryDemand,
):
    return _routing_helpers.demand(session, demand_model)
