from fastapi import APIRouter

from parsomics.entities.files.drep.router import router as drep_router
from parsomics.entities.files.fasta.router import router as fasta_router
from parsomics.entities.files.gff.router import router as gff_router

router = APIRouter(
    prefix="/files",
)

router.include_router(fasta_router)
router.include_router(gff_router)
router.include_router(drep_router)
