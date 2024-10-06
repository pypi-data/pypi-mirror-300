# -*- coding: utf-8 -*-
import logging
import os

from typing import List, Optional

from previsedx_esopredict_qc_utils import constants
from previsedx_esopredict_qc_utils.esopredict.analysis.results.file.dataset import Dataset
from previsedx_esopredict_qc_utils.esopredict.analysis.results.file.file import File as ResultsFile
from previsedx_esopredict_qc_utils.esopredict.analysis.results.file.xlsx.parser import Parser
from previsedx_esopredict_qc_utils.esopredict.analysis.results.file.record import Record as ResultsRecord
from previsedx_esopredict_qc_utils.file_utils import get_file_list


class Helper:
    """Class for helping to retrieve the appropriate Esopredict Analysis
    Results files."""

    def __init__(self, **kwargs):
        """Constructor for Helper."""
        self.analysis_record = kwargs.get("analysis_record", None)
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.indir = kwargs.get("indir", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        if (
            self.analysis_record is not None
            and self.analysis_record.analysis_id is not None
        ):
            self.analysis_id = self.analysis_record.analysis_id

        # Only process these file types.
        self._actin_file = None
        self._hpp1_file = None
        self._p16_file = None
        self._fbn1_file = None
        self._runx3_file = None

        self._actin_file_ctr = 0
        self._hpp1_file_ctr = 0
        self._p16_file_ctr = 0
        self._fbn1_file_ctr = 0
        self._runx3_file_ctr = 0

        self._dataset = None
        self.input_file_format = None
        self.is_run_dos2unix = False

        self._set_input_file_format()

        logging.info(f"Instantiated Helper in file '{os.path.abspath(__file__)}'")

    def _set_input_file_format(self) -> None:
        format = self.config.get("input_gene_files", None).get("format", None)
        if format is None or format == "":
            raise Exception(
                f"input_gene_files.format is not defined in the configuration file '{self.config_file}'"
            )
        if format == "tsv" or format == "tsv" or format == "xlsx" or format == "xls":
            self.input_file_format = format
            if format == "tsv" or format == "tsv":
                self._set_run_dos2unix()
        else:
            raise Exception(f"format '{format}' is not supported")

    def _set_run_dos2unix(self) -> None:
        run = self.config.get("run_dos2unix", None)
        if run is None or run == "":
            raise Exception(
                f"run_dos2unix is not defined in the configuration file '{self.config_file}'"
            )
        self.is_run_dos2unix = run is True

    def _get_results_files(self, indir: str) -> None:
        file_list = None

        file_list = get_file_list(indir, extension=self.input_file_format)

        if file_list is None or len(file_list) == 0:
            raise Exception(
                f"Did not find any files with extension '{self.input_file_format}' in directory '{indir}'"
            )

        results_file_list = []

        for f in file_list:
            if f.endswith(".validation-report.txt"):
                logging.info(f"Going to ignore validation report file '{f}'")
                continue

            logging.info(f"Found analyis results file '{f}'")
            basename = os.path.splitext(os.path.basename(f))[0]

            # Given file basename e.g.: P16_ID23-0085_02072024_FP.txt
            # run_id: ID23-0085
            # analysis_date: 02072024
            # analysis_id: ID23-0085_02072024
            # lab_tech_initials: FP
            parts = basename.split("_")
            if len(parts) != 4:
                raise Exception(
                    f"file basename '{basename}' is not in the correct format"
                )

            if parts[0].upper() not in constants.GENE_NAMES:
                logging.info(
                    f"Ignoring file '{f}' because gene name '{parts[0]}' is not in the list of expected gene names"
                )
                continue

            if self.input_file_format == "tsv" or self.input_file_format == "txt":
                if self.is_run_dos2unix:
                    self._run_dos2unix(f)

            results_file = ResultsFile(
                run_id=parts[1],
                analysis_date=parts[2],
                analysis_id=f"{parts[1]}-{parts[2]}",
                lab_tech_initials=parts[3],
                gene=parts[0],
                path=f,
                basename=basename,
            )

            logging.info(f"Created ResultsFile object '{results_file}'")

            results_file_list.append(results_file)

        return results_file_list

    def _run_dos2unix(self, tab_file: str) -> None:
        logging.info(f"Will attempt to run dos2unix on tab-delimited file '{tab_file}'")
        os.system(f"dos2unix {tab_file}")

    def _check_file_counts(self) -> None:
        error_ctr = 0

        if self._actin_file_ctr == 0:
            logging.error(f"Did not find ACTIN file for in directory '{self.indir}'")
            error_ctr += 1
        elif self._actin_file_ctr > 4:
            logging.error(f"Found more than 4 ACTIN file in directory '{self.indir}'")
            error_ctr += 1

        if self._hpp1_file_ctr == 0:
            logging.error(f"Did not find HPP1 file for in directory '{self.indir}'")
            error_ctr += 1
        elif self._hpp1_file_ctr > 1:
            logging.error(f"Found more than one HPP1 file in directory '{self.indir}'")
            error_ctr + 1

        if self._fbn1_file_ctr == 0:
            logging.error(f"Did not find FBN1 file for in directory '{self.indir}'")
            error_ctr += 1
        elif self._fbn1_file_ctr > 1:
            logging.error(f"Found more than one FBN1 file in directory '{self.indir}'")
            error_ctr + 1

        if self._p16_file_ctr == 0:
            logging.error(f"Did not find P16 file for in directory '{self.indir}'")
            error_ctr += 1
        elif self._p16_file_ctr > 1:
            logging.error(f"Found more than one P16 file in directory '{self.indir}'")
            error_ctr + 1

        if self._runx3_file_ctr == 0:
            logging.error(f"Did not find RUNX3 file for in directory '{self.indir}'")
            error_ctr += 1
        elif self._runx3_file_ctr > 1:
            logging.error(f"Found more than one RUNX3 file in directory '{self.indir}'")
            error_ctr + 1

        if error_ctr > 0:
            logging.warning(
                f"Encountered '{error_ctr}' errors while processing files in directory '{self.indir}'"
            )
        else:
            logging.info(
                f"Seem to have found the required files in directory '{self.indir}'"
            )

    def get_dataset(self, indir: Optional[str] = None) -> None:
        """Get the list of files in the specified directory.

        Args:
            indir (str): the directory to search for files
            extension (str): the file extension to filter on

        Returns:
            file_list (List[str]): the list of files found in the directory
        """
        if indir is None or indir == "":
            indir = self.indir

        if indir is None or indir == "":
            raise Exception("indir was not defined")

        self.indir = indir

        if self._dataset is None:
            results_file_list = self._get_results_files(indir)

            file_ctr = 0

            run_id_to_actin_results_file_lookup = {}
            run_id_to_fbn1_results_file_lookup = {}
            run_id_to_hpp1_results_file_lookup = {}
            run_id_to_p16_results_file_lookup = {}
            run_id_to_runx3_results_file_lookup = {}

            for results_file in results_file_list:
                logging.info(f"Processing results file '{results_file.path}'")

                file_ctr += 1

                if results_file.gene == "ACTIN":
                    run_id_to_actin_results_file_lookup[
                        results_file.run_id
                    ] = results_file
                    self._actin_file_ctr += 1

                elif results_file.gene == "HPP1":
                    if self._hpp1_file_ctr > 0:
                        logging.warning(
                            f"Found multiple HPP1 files '{results_file.path}'"
                        )
                    run_id_to_hpp1_results_file_lookup[
                        results_file.run_id
                    ] = results_file
                    self._hpp1_file_ctr += 1

                elif results_file.gene == "P16":
                    if self._p16_file_ctr > 0:
                        logging.warning(
                            f"Found multiple P16 files '{results_file.path}'"
                        )
                    run_id_to_p16_results_file_lookup[
                        results_file.run_id
                    ] = results_file
                    self._p16_file_ctr += 1

                elif results_file.gene == "FBN1":
                    if self._fbn1_file_ctr > 0:
                        logging.warning(
                            f"Found multiple FBN1 files '{results_file.path}'"
                        )
                    run_id_to_fbn1_results_file_lookup[
                        results_file.run_id
                    ] = results_file
                    self._fbn1_file_ctr += 1

                elif results_file.gene == "RUNX3":
                    if self._runx3_file_ctr > 0:
                        logging.warning(
                            f"Found multiple RUNX3 files '{results_file.path}'"
                        )
                    run_id_to_runx3_results_file_lookup[
                        results_file.run_id
                    ] = results_file
                    self._runx3_file_ctr += 1

                else:
                    logging.warning(f"Encountered unknown file '{results_file.path}'")

            logging.info(
                f"Processed '{file_ctr}' files found in directory '{self.indir}'"
            )

            self._check_file_counts()

            dataset = Dataset(
                run_id=results_file_list[0].run_id,
                indir=self.indir,
                actin_file_count=self._actin_file_ctr,
                fbn1_file_count=self._fbn1_file_ctr,
                hpp1_file_count=self._hpp1_file_ctr,
                p16_file_count=self._p16_file_ctr,
                runx3_file_count=self._runx3_file_ctr,
                run_id_to_actin_file_lookup=run_id_to_actin_results_file_lookup,
                run_id_to_fbn1_file_lookup=run_id_to_fbn1_results_file_lookup,
                run_id_to_hpp1_file_lookup=run_id_to_hpp1_results_file_lookup,
                run_id_to_p16_file_lookup=run_id_to_p16_results_file_lookup,
                run_id_to_runx3_file_lookup=run_id_to_runx3_results_file_lookup,
            )

            self._dataset = dataset
            return self._dataset

    def get_gene_file_records(self, gene_file: str) -> List[ResultsRecord]:
        """Parse the gene file and return the records.

        Args:
            gene_file (str): the gene file to parse
        """
        if gene_file.path.endswith(".xlsx") or gene_file.path.endswith(".xls"):
            parser = Parser(
                config=self.config,
                config_file=self.config_file,
                logfile=self.logfile,
                outdir=self.outdir,
                verbose=self.verbose,
            )

        else:
            raise Exception(f"Unknown file type for gene file: '{gene_file}'")

        # Get the records for each sample identifier
        return parser.get_records(gene_file.path)
