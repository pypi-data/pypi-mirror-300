from fastapi import APIRouter

from parsomics.entities.workflow.project.router import router as project_router
from parsomics.entities.workflow.run.router import router as run_router
from parsomics.entities.workflow.source.router import router as source_router
from parsomics.entities.workflow.tool.router import router as tool_router

router = APIRouter(
    prefix="/workflow",
)

router.include_router(project_router)
router.include_router(run_router)
router.include_router(source_router)
router.include_router(tool_router)
