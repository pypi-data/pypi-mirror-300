from typing import Any

from fastapi import HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select


class RoutingHelpers(BaseModel):
    table_type: type
    transactions: Any

    def read(
        self,
        session: Session,
        offset: int = 0,
        limit: int = Query(default=100, le=100),
    ):
        statement = select(self.table_type).offset(offset).limit(limit)
        reads = session.exec(statement).all()
        return reads

    def create(
        self,
        session: Session,
        create_model: Any,
    ):
        created = self.transactions.create(session, create_model)

        if not created:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create {create_model}",
            )

        return created

    def demand(
        self,
        session: Session,
        demand_model: Any,
    ):
        demanded = self.transactions.demand(session, demand_model)

        if not demanded:
            raise HTTPException(
                status_code=500, detail=f"Failed to demand {demand_model}"
            )

        return demanded
