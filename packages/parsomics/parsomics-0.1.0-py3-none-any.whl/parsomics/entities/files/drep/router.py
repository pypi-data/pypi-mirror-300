from fastapi import APIRouter

from parsomics.entities.files.drep.directory.router import router as directory_router
from parsomics.entities.files.drep.entry.router import router as entry_router

router = APIRouter(
    prefix="/drep",
)

router.include_router(directory_router)
router.include_router(entry_router)
