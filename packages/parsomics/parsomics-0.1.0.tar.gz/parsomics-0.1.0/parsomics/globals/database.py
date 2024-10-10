# isort: off

# NOTE: for SQLModel.create_all() to work, SQLModel and all models need to
#       be imported before the database engine object. Importing them here
#       guarantees that happens, as recommended by the documentation:
#       https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#calling-create_all

import keyring
from sqlmodel import SQLModel

# Files
from parsomics.entities.files.fasta.file.models import *
from parsomics.entities.files.fasta.entry.models import *
from parsomics.entities.files.gff.file.models import *
from parsomics.entities.files.gff.entry.models import *
from parsomics.entities.files.drep.directory.models import *
from parsomics.entities.files.drep.entry.models import *
from parsomics.entities.files.gtdbtk_tsv.file.models import *
from parsomics.entities.files.gtdbtk_tsv.entry.models import *
from parsomics.entities.files.protein_annotation.file.models import *
from parsomics.entities.files.protein_annotation.entry.models import *
from parsomics.entities.files.gene_annotation.file.models import *
from parsomics.entities.files.gene_annotation.entry.models import *

# Omics
from parsomics.entities.omics.gene.models import *
from parsomics.entities.omics.repeated_region.models import *
from parsomics.entities.omics.contig.models import *
from parsomics.entities.omics.fragment.models import *
from parsomics.entities.omics.genome.models import *
from parsomics.entities.omics.protein.models import *
from parsomics.entities.omics.fragment_protein_link.models import *
from parsomics.entities.omics.genome_cluster.models import *
from parsomics.entities.omics.sample.models import *

# Workflow
from parsomics.entities.workflow.metadata.models import *
from parsomics.entities.workflow.project.models import *
from parsomics.entities.workflow.assembly.models import *
from parsomics.entities.workflow.run.models import *
from parsomics.entities.workflow.tool.models import *
from parsomics.entities.workflow.source.models import *

# isort: on

from sqlalchemy.engine import URL
from sqlmodel import Session, create_engine

DATABASE_NAME = "parsomics"

# Infrastructure
DBMS_NAME = "postgresql"
DBMS_DRIVER = "psycopg2"

# Credentials
USERNAME = "admin"
PASSWORD = keyring.get_password(DATABASE_NAME, USERNAME)

DATABASE_URL = URL.create(
    drivername=f"{DBMS_NAME}+{DBMS_DRIVER}",
    username=USERNAME,
    password=PASSWORD,
    host="localhost",
    database=DATABASE_NAME,
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    executemany_mode="values_plus_batch",
    insertmanyvalues_page_size=10000,
    executemany_batch_page_size=2000,
)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
