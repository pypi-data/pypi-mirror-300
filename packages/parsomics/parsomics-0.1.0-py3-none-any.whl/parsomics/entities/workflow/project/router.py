from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics.entities.common.routing_helpers import RoutingHelpers
from parsomics.entities.workflow.project.models import (
    Project,
    ProjectCreate,
    ProjectDemand,
    ProjectPublic,
)
from parsomics.entities.workflow.project.transactions import ProjectTransactions
from parsomics.globals.database import get_session

_routing_helpers = RoutingHelpers(
    table_type=Project,
    transactions=ProjectTransactions(),
)
router = APIRouter(
    prefix="/project",
    tags=["workflow/project"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/", response_model=list[ProjectPublic])
def read_projects(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)


@router.post("/create", response_model=ProjectPublic)
def create_project(
    *,
    session: Session = Depends(get_session),
    create_model: ProjectCreate,
):
    return _routing_helpers.create(session, create_model)


@router.post("/demand", response_model=ProjectPublic)
def demand_project(
    *,
    session: Session = Depends(get_session),
    demand_model: ProjectDemand,
):
    return _routing_helpers.demand(session, demand_model)
