from fastapi import APIRouter

from parsomics.entities.files.gff.entry.router import router as entry_router
from parsomics.entities.files.gff.file.router import router as file_router

router = APIRouter(
    prefix="/gff",
)

router.include_router(file_router)
router.include_router(entry_router)
