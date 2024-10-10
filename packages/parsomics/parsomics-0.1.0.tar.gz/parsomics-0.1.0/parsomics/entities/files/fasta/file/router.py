from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics.entities.common.routing_helpers import RoutingHelpers
from parsomics.entities.files.fasta.file.models import (
    FASTAFile,
    FASTAFileCreate,
    FASTAFileDemand,
    FASTAFilePublic,
)
from parsomics.entities.files.fasta.file.transactions import FASTAFileTransactions
from parsomics.globals.database import get_session

_routing_helpers = RoutingHelpers(
    table_type=FASTAFile,
    transactions=FASTAFileTransactions(),
)
router = APIRouter(
    prefix="/file",
    tags=["files/fasta/file"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/", response_model=list[FASTAFilePublic])
def read_files(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)


@router.post("/create", response_model=FASTAFilePublic)
def create_file(
    *,
    session: Session = Depends(get_session),
    create_model: FASTAFileCreate,
):
    return _routing_helpers.create(session, create_model)


@router.post("/demand", response_model=FASTAFilePublic)
def demand_file(
    *,
    session: Session = Depends(get_session),
    demand_model: FASTAFileDemand,
):
    return _routing_helpers.demand(session, demand_model)
