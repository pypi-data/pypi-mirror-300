"""Class for parsing Thermo Fisher Scientific QuantStudio qPCR Result Excel
files."""

import logging
import os
import sys
from datetime import datetime
from typing import List

import pandas as pd
from pydantic import ValidationError

from previsedx_esopredict_qc_utils import constants
from previsedx_esopredict_qc_utils.esopredict.analysis.results.file.record import Record
from previsedx_esopredict_qc_utils.file_utils import check_infile_status


# Need to install the following package to read Excel files with .xls extension.
# pip install xlrd==2.0.1


class Parser:
    """Class for parsing Thermo Fisher Scientific QuantStudio qPCR Result Excel
    files."""

    def __init__(self, **kwargs):
        """Constructor for Parser."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self.is_parsed = False
        self.rec_ctr = 0
        self.rec_list = []

        self.error_ctr = 0
        self.error_list = []

        logging.info(f"Instantiated Parser in file '{os.path.abspath(__file__)}'")

    def get_records(self, infile: str) -> List[Record]:
        """Parser the tab-delimited file and retrieve a list of records.

        Args:
            infile (str): The tab-delimited results to be parsed.
        Returns:
            List(Record): The parsed records.
        """
        if self.is_parsed:
            return self.rec_list

        logging.info(f"Will attempt to parse gene file '{infile}'")

        check_infile_status(infile)

        record_ctr = 0

        sheet_name = self.config.get("gene_file", None).get("sheet_name", None)
        if sheet_name is None or sheet_name == "":
            sheet_name = constants.DEFAULT_RESULTS_SHEET_NAME
        logging.info(f"sheet_name: {sheet_name}")

        header_row_number = self.config.get("gene_file", None).get(
            "header_row_number", None
        )
        if header_row_number is None or header_row_number == "":
            header_row_number = constants.DEFAULT_HEADER_ROW_NUMBER
        logging.info(f"header_row_number: {header_row_number}")

        # Read the Excel file
        df = pd.read_excel(
            infile,
            sheet_name=sheet_name,
            header=header_row_number,
            engine="xlrd",  # Need to install the following package to read Excel files with .xls extension: pip install xlrd==2.0.1
        )

        # Check if the expected columns are present
        expected_columns = [
            "Well",
            "Well Position",
            "Sample Name",
            "Target Name",
            "Quantity",
            "Quantity Mean",
            "Quantity SD",
            "Y-Intercept",
            "R(superscript 2)",
            "Slope",
            "Efficiency",
            "Amp Status",
        ]

        missing_columns = [col for col in expected_columns if col not in df.columns]

        if missing_columns:
            raise Exception(f"Missing columns in the DataFrame: {missing_columns} while processing file '{os.path.basename(infile)}'")

        # Remove all records where all cells are empty
        df = df.dropna(how="all")

        # Extract the relevant rows and columns
        df = df.loc[0:, expected_columns]

        # Replace NaN values with an empty string
        # df.fillna(0.0, inplace=True)

        record_number = 0

        for index, row in df.iterrows():
            record_number += 1

            row_dict = row.to_dict()

            try:
                record = Record(**row_dict)

                self.rec_list.append(record)

                self.rec_ctr += 1

            except ValidationError as exc:
                print(repr(exc.errors()[0]["type"]))
                missing_fields = [
                    error["loc"][0]
                    for error in exc.errors()
                    if error["msg"] == "field required"
                ]
                print("Missing fields:", missing_fields)
                print(exc.errors())
                sys.exit(1)
                # > 'missing'

            except Exception as e:
                if (row["Quantity Mean"] is None or row["Quantity Mean"] == "") and (
                    row["Sample Name"] in ("STD 1", "STD 2", "STD 3", "STD 4", "STD 5")
                    or row["Sample Name"].startswith("NTC - REP")
                    or row["Sample Name"] == "EXTRACT NEG"
                    or row["Sample Name"] == "NTC"
                ):
                    logging.warning(
                        f"Encountered a record with no quantity mean value for sample name '{row['Sample Name']}'"
                    )
                elif (row["Quantity Mean"] is None or row["Quantity Mean"] == "") and (
                    row["Sample Name"] is None or row["Sample Name"] == ""
                ):
                    logging.error(
                        "Encountered a record with no quantity mean value and no sample name"
                    )
                else:
                    logging.error(
                        f"Encountered some exception with record number '{record_number}': {e}"
                    )
                    raise e
                    self.error_ctr += 1
                    self.error_list.append(e)

                sys.exit(1)
            record_ctr += 1

        logging.info(f"Processed '{record_ctr}' records in data file '{infile}'")

        if self.error_ctr > 0:
            self._write_validation_report(infile)
            sys.exit(1)

        self.is_parsed = True
        return self.rec_list

    # TODO: move this method into the base class
    def _write_validation_report(self, infile: str) -> None:
        """Write the validation report file.

        Args:
            infile (str): The input QuantStudio qPCR Results file that was parsed.
        """
        logging.info(f"Will attempt to generate validation report for file '{infile}'")

        basename = os.path.basename(infile)

        outfile = os.path.join(self.outdir, f"{basename}.validation-report.txt")

        with open(outfile, "w") as of:
            of.write(f"## method-created: {os.path.abspath(__file__)}\n")
            of.write(
                f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n"
            )
            of.write(f"## created-by: {os.environ.get('USER')}\n")
            of.write(f"## infile: {infile}\n")
            of.write(f"## logfile: {self.logfile}\n")

            if self.error_ctr > 0:
                of.write(
                    f"Encountered the following '{self.error_ctr}' validation errors:\n"
                )
                for error in self.error_list:
                    of.write(f"{error}\n")

        logging.info(f"Wrote file validation report file '{outfile}'")
        if self.verbose:
            print(f"Wrote file validation report file '{outfile}'")
