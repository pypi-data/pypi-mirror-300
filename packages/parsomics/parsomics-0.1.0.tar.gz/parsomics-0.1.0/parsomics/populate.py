import datetime as dt
import logging
from pathlib import Path
from typing import Any, Callable, Sequence

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from timeit_decorator import timeit

# Files
from parsomics.entities.workflow.common.progress import ProgressStatus
from parsomics.entities.files.drep.directory.models import DrepDirectory
from parsomics.entities.files.drep.entry.models import DrepEntry, DrepEntryPublic
from parsomics.entities.files.fasta.entry.models import FASTAEntry
from parsomics.entities.files.fasta.file.models import FASTAFile
from parsomics.entities.files.fasta.sequence_type import SequenceType
from parsomics.entities.files.gff.entry.models import GFFEntry

# Workflow
from parsomics.entities.omics.contig.models import Contig
from parsomics.entities.omics.fragment.common.fragment_type import FragmentType
from parsomics.entities.omics.fragment.models import Fragment
from parsomics.entities.omics.fragment_protein_link.models import FragmentProteinLink
from parsomics.entities.omics.gene.models import Gene
from parsomics.entities.omics.genome.models import Genome
from parsomics.entities.omics.genome_cluster.models import (
    GenomeClusterDemand,
    GenomeClusterPublic,
)
from parsomics.entities.omics.genome_cluster.transactions import (
    GenomeClusterTransactions,
)
from parsomics.entities.omics.protein.models import Protein
from parsomics.entities.omics.repeated_region.models import RepeatedRegion
from parsomics.entities.omics.sample.models import SampleDemand, SamplePublic
from parsomics.entities.omics.sample.transactions import SampleTransactions
from parsomics.entities.workflow.assembly.models import Assembly, AssemblyDemand
from parsomics.entities.workflow.assembly.transactions import AssemblyTransactions
from parsomics.entities.workflow.metadata.models import Metadata, MetadataDemand
from parsomics.entities.workflow.metadata.transactions import MetadataTransactions
from parsomics.entities.workflow.project.models import (
    Project,
    ProjectDemand,
)
from parsomics.entities.workflow.project.transactions import ProjectTransactions
from parsomics.entities.workflow.run.models import Run, RunDemand
from parsomics.entities.workflow.run.transactions import RunTransactions
from parsomics.entities.workflow.tool.models import ToolDemand
from parsomics.entities.workflow.tool.transactions import ToolTransactions
from parsomics.globals.database import engine

# Processors
from parsomics.processors.drep_processor import DrepOutputProcessor
from parsomics.processors.gtdbtk_processor import GTDBTkOutputProcessor
from parsomics.processors.prokka_processor import ProkkaOutputProcessor

# Globals


def _batch_insert(session, model, mappings):
    try:
        session.bulk_insert_mappings(model, mappings)
        session.commit()
    except IntegrityError as e:
        logging.warning(
            f"Ignored duplicated and/or invalid entry for {model}. Exception caught: {e}"
        )
        session.rollback()


@timeit()
def populate_clusters_samples_and_genomes(session):
    statement = select(DrepEntry)
    drep_entries = session.exec(statement).all()

    mappings = []
    for drep_entry in drep_entries:
        drep_entry_public = DrepEntryPublic.model_validate(drep_entry)

        genome_name = drep_entry_public.genome_name
        sample_name = genome_name.split(".bin")[0]
        genome_cluster_name = drep_entry_public.genome_cluster_name
        drep_directory_key = drep_entry_public.directory_key
        drep_entry_key = drep_entry_public.key

        # demand sample
        sample_demand_model: SampleDemand = SampleDemand(
            name=sample_name,
            drep_directory_key=drep_directory_key,
        )
        sample: SamplePublic = SampleTransactions().demand(
            session,
            sample_demand_model,
        )
        sample_key: int = sample.key

        # demand genome cluster
        genome_cluster_create_model: GenomeClusterDemand = GenomeClusterDemand(
            name=genome_cluster_name,
            drep_directory_key=drep_directory_key,
        )
        genome_cluster: GenomeClusterPublic = GenomeClusterTransactions().demand(
            session,
            genome_cluster_create_model,
        )
        genome_cluster_key = genome_cluster.key

        mappings.append(
            {
                "drep_entry_key": drep_entry_key,
                "genome_cluster_key": genome_cluster_key,
                "sample_key": sample_key,
            }
        )
    _batch_insert(session, Genome, mappings)


@timeit()
def populate_contigs(session):
    statement = (
        select(FASTAEntry)
        .join(FASTAFile)
        .where(FASTAFile.sequence_type == SequenceType.CONTIG)
    )
    fasta_contig_entries = session.exec(statement).all()

    mappings = []
    for fasta_contig_entry in fasta_contig_entries:
        mappings.append(
            {
                "fasta_entry_key": fasta_contig_entry.key,
                "genome_key": fasta_contig_entry.file.genome.key,
            }
        )
    _batch_insert(session, Contig, mappings)


@timeit()
def populate_genes(session):
    statement = select(GFFEntry).where(
        GFFEntry.fragment_type == FragmentType.GENE,
    )
    gff_gene_entries = session.exec(statement).all()

    gene_name_to_contig_key: dict[str, int] = {}
    contig_name_to_contig_key: dict[str, int] = {}
    for gff_gene_entry in gff_gene_entries:
        contig_name = gff_gene_entry.contig_name
        gene_name = gff_gene_entry.gene_name

        if contig_name not in contig_name_to_contig_key:
            statement = (
                select(Contig)
                .join(FASTAEntry)
                .where(
                    FASTAEntry.sequence_name == contig_name,
                )
            )
            contigs = session.exec(statement).all()

            if len(contigs) > 1:
                logging.warning(
                    f"Expected only one Contig to match name {contig_name}, "
                    f"but matched: {contigs}"
                )
            if not contigs:
                logging.warning(f"No Contigs were matched to name {contig_name}")
            else:
                contig_name_to_contig_key[contig_name] = contigs[0].key

        if contig_name in contig_name_to_contig_key:
            gene_name_to_contig_key[gene_name] = contig_name_to_contig_key[contig_name]

    statement = (
        select(FASTAEntry)
        .join(FASTAFile)
        .where(FASTAFile.sequence_type == SequenceType.GENE)
    )
    fasta_gene_entries = session.exec(statement).all()

    mappings = []
    for fasta_gene_entry in fasta_gene_entries:
        gene_name = fasta_gene_entry.sequence_name
        contig_key = gene_name_to_contig_key[gene_name]

        mappings.append(
            {
                "fasta_entry_key": fasta_gene_entry.key,
                "contig_key": contig_key,
            }
        )
    _batch_insert(session, Gene, mappings)


@timeit()
def populate_repeated_region(session):
    statement = select(GFFEntry).where(
        GFFEntry.fragment_type == FragmentType.REPEAT_REGION,
    )
    gff_entries = session.exec(statement).all()

    mappings = []
    contig_name_to_contig_key: dict[str, int] = {}
    for gff_entry in gff_entries:
        contig_name = gff_entry.contig_name

        if contig_name not in contig_name_to_contig_key:
            statement = (
                select(Contig)
                .join(FASTAEntry)
                .where(
                    FASTAEntry.sequence_name == contig_name,
                )
            )
            contigs = session.exec(statement).all()

            if len(contigs) > 1:
                logging.warning(
                    f"Expected only one Contig to match name {contig_name}, "
                    f"of the GFFEntry {gff_entry}, but matched: {contigs}"
                )

            if not contigs:
                logging.warning(
                    f"No Genes were matched to name {contig_name}, of the "
                    f"GFFEntry {gff_entry}"
                )
            else:
                contig_key = contigs[0].key
                contig_name_to_contig_key[contig_name] = contig_key

        if contig_name in contig_name_to_contig_key:
            contig_key = contig_name_to_contig_key[contig_name]
            mappings.append(
                {
                    "gff_entry_key": gff_entry.key,
                    "contig_key": contig_key,
                }
            )
    _batch_insert(session, RepeatedRegion, mappings)


@timeit()
def populate_fragments(session):
    # exclude FragmentTypes that have their own tables
    statement = select(GFFEntry).where(
        GFFEntry.fragment_type != FragmentType.GENE,
        GFFEntry.fragment_type != FragmentType.REPEAT_REGION,
    )
    gff_entries = session.exec(statement).all()

    mappings = []
    gene_name_to_gene_key: dict[str, int] = {}
    for gff_entry in gff_entries:
        gene_name = gff_entry.gene_name

        if gene_name not in gene_name_to_gene_key:
            statement = (
                select(Gene)
                .join(FASTAEntry)
                .where(
                    FASTAEntry.sequence_name == gene_name,
                )
            )
            genes = session.exec(statement).all()

            if len(genes) > 1:
                logging.warning(
                    f"Expected only one Gene to match name {gene_name}, "
                    f"of the GFFEntry {gff_entry}, but matched: {genes}"
                )

            if not genes:
                logging.warning(
                    f"No Genes were matched to name {gene_name}, of the "
                    f"GFFEntry {gff_entry}"
                )
            else:
                gene_key = genes[0].key
                gene_name_to_gene_key[gene_name] = gene_key

        if gene_name in gene_name_to_gene_key:
            gene_key = gene_name_to_gene_key[gene_name]
            mappings.append(
                {
                    "gff_entry_key": gff_entry.key,
                    "gene_key": gene_key,
                }
            )
    _batch_insert(session, Fragment, mappings)


@timeit()
def populate_proteins(session):
    statement = (
        select(FASTAEntry)
        .join(FASTAFile)
        .where(FASTAFile.sequence_type == SequenceType.PROTEIN)
    )
    fasta_protein_entries = session.exec(statement).all()
    mappings = [
        {"fasta_entry_key": fasta_protein_entry.key}
        for fasta_protein_entry in fasta_protein_entries
    ]
    _batch_insert(session, Protein, mappings)


@timeit()
def populate_fragment_protein_links(session):
    statement = (
        select(Fragment)
        .join(GFFEntry)
        .where(GFFEntry.fragment_type == FragmentType.CDS)
    )
    cdss = session.exec(statement).all()

    mappings = []
    gene_name_to_protein_key: dict[str, int] = {}
    for cds in cdss:
        gene_name = cds.gff_entry.gene_name

        if gene_name not in gene_name_to_protein_key:
            statement = (
                select(Protein).join(FASTAEntry)
                # NOTE: in prokaryotes, there's a 1:1 relationship between genes
                #       and proteins. For that reason, prokka names each protein
                #       with the same name as the gene that encodes them.
                .where(FASTAEntry.sequence_name == cds.gff_entry.gene_name)
            )
            proteins = session.exec(statement).all()

            if len(proteins) > 1:
                logging.warning(
                    f"Expected only one Protein to match name {cds.gff_entry.gene_name}, "
                    f"but matched: {proteins}"
                )

            if not proteins:
                logging.warning(f"No Proteins were matched to name {cds.gene_name} ")
            else:
                protein_key = proteins[0].key
                gene_name_to_protein_key[gene_name] = protein_key

        if gene_name in gene_name_to_protein_key:
            protein_key = gene_name_to_protein_key[gene_name]
            mappings.append(
                {
                    "fragment_key": cds.key,
                    "protein_key": protein_key,
                }
            )

    _batch_insert(session, FragmentProteinLink, mappings)


def _get_tool_key(tool_name) -> int:
    tool_demand_model = ToolDemand(name=tool_name)
    with Session(engine) as session:
        tool_key = ToolTransactions().demand(session, tool_demand_model).key
    return tool_key


def _get_run_key(run_info: dict, assembly_key: int, tool_key: int) -> int:
    # Parse the variables in the run configuration
    output_directory = run_info["output_directory"]

    version: str | None = None
    if "version" in run_info:
        version = run_info["version"]

    date: dt.date | None = None
    if "date" in run_info:
        date = dt.datetime.strptime(run_info["date"], "%d/%m/%Y").date()

    # Create the Run
    run_demand_model = RunDemand(
        output_directory=output_directory,
        version=version,
        date=date,
        tool_key=tool_key,
        assembly_key=assembly_key,
    )
    with Session(engine) as session:
        run = RunTransactions().demand(session, run_demand_model)
        run.status = ProgressStatus.IN_PROGRESS
        session.commit()
        run_key = run.key

    return run_key


def process_files(
    run_info: dict,
    assembly_key: int,
    dereplicated_genomes: Sequence[str],
    tool_name: str,
    process_files_func: Callable[[str, int, int, int, Sequence[str]], None],
) -> None:
    # Tool
    tool_key = _get_tool_key(tool_name)

    # Run
    if "output_directory" not in run_info:
        raise Exception(
            f'Mandatory "output_directory" field not in {tool_name} '
            f"configuration: {run_info}"
        )
    run_key = _get_run_key(run_info, assembly_key, tool_key)

    # Files and Entries
    output_directory = run_info["output_directory"]
    process_files_func(
        output_directory, assembly_key, run_key, tool_key, dereplicated_genomes
    )

    # Update progress status for Run
    with Session(engine) as session:
        run = session.get(Run, run_key)
        if not run:
            raise Exception(f"Unexpectedly unable to get Run with key {run_key}")
        run.status = ProgressStatus.DONE
        session.commit()


def _get_dereplicated_genomes(drep_run_info) -> Sequence[str]:
    output_directory = drep_run_info["output_directory"]
    output_results_directory = str(
        Path(output_directory) / Path("dRep_results") / Path("data_tables")
    )

    dereplicated_genomes: Sequence[str]
    with Session(engine) as session:
        statement = (
            select(DrepEntry.genome_name)
            .join(DrepDirectory)
            .where(DrepDirectory.path == output_results_directory)
        )
        results = session.exec(statement)
        dereplicated_genomes = results.all()

    if not dereplicated_genomes:
        raise Exception(
            f"No dereplicated genomes were found in {output_results_directory}"
        )

    return dereplicated_genomes


@timeit()
def populate_drep(run_info: dict, assembly_key: int) -> None:
    def process_drep_files(
        output_directory, assembly_key, run_key, tool_key, dereplicated_genomes
    ):
        output_results_directory = str(
            Path(output_directory) / Path("dRep_results") / Path("data_tables")
        )
        drep_output_processor = DrepOutputProcessor(
            output_directory=output_results_directory,
            run_key=run_key,
        )
        drep_output_processor.process_drep_directory(engine)

    process_files(run_info, assembly_key, [], "drep", process_drep_files)


@timeit()
def populate_gtdbtk(
    run_info: dict, assembly_key: int, dereplicated_genomes: Sequence[str]
) -> None:
    def process_gtdbtk_files(
        output_directory, assembly_key, run_key, tool_key, dereplicated_genomes
    ):

        output_results_directory = str(
            Path(output_directory) / Path("results") / Path("classify")
        )
        gtdbtk_output_processor = GTDBTkOutputProcessor(
            output_directory=output_results_directory,
            assembly_key=assembly_key,
            run_key=run_key,
            tool_key=tool_key,
            dereplicated_genomes=dereplicated_genomes,
        )
        gtdbtk_output_processor.process_gtdbtk_tsv_files(engine)

    process_files(
        run_info, assembly_key, dereplicated_genomes, "gtdbtk", process_gtdbtk_files
    )


@timeit()
def populate_prokka(
    run_info: dict, assembly_key: int, dereplicated_genomes: Sequence[str]
) -> None:
    def process_prokka_files(
        output_directory, assembly_key, run_key, tool_key, dereplicated_genomes
    ):
        prokka_output_processor = ProkkaOutputProcessor(
            output_directory=output_directory,
            assembly_key=assembly_key,
            run_key=run_key,
            tool_key=tool_key,
            dereplicated_genomes=dereplicated_genomes,
        )
        prokka_output_processor.process_fasta_files(engine)
        prokka_output_processor.process_gff_files(engine)

    process_files(
        run_info, assembly_key, dereplicated_genomes, "prokka", process_prokka_files
    )


@timeit()
def populate_all(
    config: dict[str, Any],
    plugin_name_to_populate: dict[str, Callable] = {},
):
    plugin_names: list[str] = config["plugins"]

    # Create or update parsomics metadata table
    metadata_demand_model = MetadataDemand()
    with Session(engine) as session:
        metadata = MetadataTransactions().demand(session, metadata_demand_model)
        metadata.status = ProgressStatus.IN_PROGRESS
        session.commit()
        metadata_key = metadata.key

    for project_config in config["Project"]:

        # Create project
        project_demand_model = ProjectDemand(name=project_config["name"])
        with Session(engine) as session:
            project = ProjectTransactions().demand(session, project_demand_model)
            project.status = ProgressStatus.IN_PROGRESS
            session.commit()
            project_key = project.key
        project_config.pop("name")

        # One project may have many assemblies associated with it
        for assembly_name in project_config:
            assembly_config = project_config[assembly_name]

            assembly_demand_model = AssemblyDemand(
                project_key=project_key, name=assembly_name.upper()
            )
            with Session(engine) as session:
                assembly = AssemblyTransactions().demand(session, assembly_demand_model)
                assembly.status = ProgressStatus.IN_PROGRESS
                session.commit()
                assembly_key = assembly.key

            # Populate dRep
            if "drep" in assembly_config:
                drep_run_info = assembly_config["drep"]
                populate_drep(drep_run_info, assembly_key)
                dereplicated_genomes = _get_dereplicated_genomes(drep_run_info)
            else:
                raise Exception(
                    f"No dRep runs found in config for project {project_config['name']}"
                )

            # Populate Genomes, Samples, and Genome Clusters. This must be done at this
            # stage, so Genomes can be referenced in the foreign key of the next files
            # (FASTA, GFF, etc)
            with Session(engine) as session:
                populate_clusters_samples_and_genomes(session)

            # Populate GTDB-Tk
            if "gtdbtk" in assembly_config:
                gtdbtk_run_info = assembly_config["gtdbtk"]
                populate_gtdbtk(gtdbtk_run_info, assembly_key, dereplicated_genomes)

            # Populate prokka
            if "prokka" in assembly_config:
                prokka_run_info = assembly_config["prokka"]
                populate_prokka(prokka_run_info, assembly_key, dereplicated_genomes)

            with Session(engine) as session:
                populate_contigs(session)
                populate_genes(session)
                populate_repeated_region(session)
                populate_fragments(session)
                populate_proteins(session)
                populate_fragment_protein_links(session)

            for plugin_name in plugin_names:
                plugin_run_info = assembly_config[plugin_name]
                populate_plugin = plugin_name_to_populate[plugin_name]
                populate_plugin(plugin_run_info, assembly_key, dereplicated_genomes)

            # Update progress status for Assembly
            with Session(engine) as session:
                assembly = session.get(Assembly, assembly_key)
                if not assembly:
                    raise Exception(
                        f"Unexpectedly unable to get Assembly with key {assembly_key}"
                    )
                assembly.status = ProgressStatus.DONE
                session.commit()

        # Update progress status for Project
        with Session(engine) as session:
            project = session.get(Project, project_key)
            if not project:
                raise Exception(
                    f"Unexpectedly unable to get Project with key {project_key}"
                )
            project.status = ProgressStatus.DONE
            session.commit()

    with Session(engine) as session:
        metadata = session.get(Metadata, metadata_key)
        if not metadata:
            raise Exception(
                f"Unexpectedly unable to get Metadata with key {metadata_key}"
            )
        metadata.status = ProgressStatus.DONE
        session.commit()
