import logging
from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import Engine
from sqlmodel import Session

from parsomics.entities.files.gtdbtk_tsv.file.models import (
    GTDBTkTsvFile,
    GTDBTkTsvFileDemand,
)
from parsomics.entities.files.gtdbtk_tsv.file.transactions import (
    GTDBTkTsvFileTransactions,
)
from parsomics.entities.files.gtdbtk_tsv.file_factory import GTDBTkTsvFileFactory
from parsomics.entities.files.gtdbtk_tsv.parser import GTDBTkTsvParser
from parsomics.entities.files.gtdbtk_tsv.validated_file import GTDBTkTsvValidatedFile


class GTDBTkOutputProcessor(BaseModel):
    output_directory: str
    dereplicated_genomes: Sequence[str]
    assembly_key: int
    run_key: int
    tool_key: int

    def process_gtdbtk_tsv_files(self, engine: Engine):
        gtdbtk_tsv_file_factory: GTDBTkTsvFileFactory = GTDBTkTsvFileFactory(
            self.output_directory,
            self.dereplicated_genomes,
        )

        # BUG: this is coming out empty
        gtdbtk_tsv_files: list[GTDBTkTsvValidatedFile] = (
            gtdbtk_tsv_file_factory.assemble()
        )
        for f in gtdbtk_tsv_files:
            run_key = self.run_key

            gtdbtk_tsv_file_demand_model = GTDBTkTsvFileDemand(
                path=f.path,
                run_key=run_key,
            )

            with Session(engine) as session:
                gtdbtk_tsv_file: GTDBTkTsvFile = GTDBTkTsvFile.model_validate(
                    GTDBTkTsvFileTransactions().demand(
                        session,
                        gtdbtk_tsv_file_demand_model,
                    )
                )

            gtdbtk_tsv_parser = GTDBTkTsvParser(
                file=gtdbtk_tsv_file,
                assembly_key=self.assembly_key,
                tool_key=self.tool_key,
            )
            gtdbtk_tsv_parser.parse(engine)

        logging.info(
            f"Finished adding all GTDBTk files on {self.output_directory} to the database."
        )
