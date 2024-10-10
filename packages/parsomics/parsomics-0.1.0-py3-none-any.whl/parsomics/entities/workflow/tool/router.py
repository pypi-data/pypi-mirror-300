from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics.entities.common.routing_helpers import RoutingHelpers
from parsomics.entities.workflow.tool.models import (
    Tool,
    ToolCreate,
    ToolDemand,
    ToolPublic,
)
from parsomics.entities.workflow.tool.transactions import ToolTransactions
from parsomics.globals.database import get_session

_routing_helpers = RoutingHelpers(
    table_type=Tool,
    transactions=ToolTransactions(),
)
router = APIRouter(
    prefix="/tool",
    tags=["workflow/tool"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/", response_model=list[ToolPublic])
def read_tools(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)


@router.post("/create", response_model=ToolPublic)
def create_tool(
    *,
    session: Session = Depends(get_session),
    create_model: ToolCreate,
):
    return _routing_helpers.create(session, create_model)


@router.post("/demand", response_model=ToolPublic)
def demand_tool(
    *,
    session: Session = Depends(get_session),
    demand_model: ToolDemand,
):
    return _routing_helpers.demand(session, demand_model)
