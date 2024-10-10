from fastapi import APIRouter

from parsomics.entities.files.fasta.entry.router import router as entry_router
from parsomics.entities.files.fasta.file.router import router as file_router

router = APIRouter(
    prefix="/fasta",
)

router.include_router(file_router)
router.include_router(entry_router)
