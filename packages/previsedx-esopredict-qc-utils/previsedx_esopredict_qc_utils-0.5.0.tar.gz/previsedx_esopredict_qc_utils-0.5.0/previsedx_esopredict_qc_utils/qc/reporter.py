import logging
import os

from datetime import datetime
from typing import List
from previsedx_esopredict_qc_utils import constants
from previsedx_esopredict_qc_utils.qc.record import Record


class Reporter:
    """Class for writing the esopredict QC checks report file."""

    def __init__(self, **kwargs):
        """Constructor for Reporter"""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.logfile = kwargs.get("logfile", None)
        self.indir = kwargs.get("indir", None)
        self.outdir = kwargs.get("outdir", None)
        self.outfile = kwargs.get("outfile", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        logging.info(f"Instantiated Reporter in file '{os.path.abspath(__file__)}'")

    def generate_report(self, records: List[Record]) -> None:
        """Method to generate the QC checks report.

        Args:
            records (List[Record]): the list of records to be written to the report.
        """

        outfile = self.outfile
        if outfile is None or outfile == "":
            outfile = os.path.join(self.outdir, "qc-checks-report.txt")

        with open(outfile, 'w') as of:
            of.write(f"## method-created: {os.path.abspath(__file__)}\n")
            of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
            of.write(f"## created-by: {os.environ.get('USER')}\n")
            of.write(f"## config_file: {self.config_file}\n")
            of.write(f"## indir: {self.indir}\n")
            of.write(f"## logfile: {self.logfile}\n")

            of.write("Summary\n========\n\n")

            for record in records:
                of.write(f"({record.number}): {record.name} - {record.status}\n")
                of.write(f"\t{record.desc}\n\n")

            of.write("\nDetails\n========\n\n")

            for record in records:
                of.write("=====================================================================\n")
                of.write(f"# Check Category Number: {record.number}\n")
                of.write(f"# Check Name: {record.name}\n")
                of.write(f"# Description: {record.desc}\n")
                of.write(f"# Overall Status: {record.status}\n")
                of.write("=====================================================================\n")

                if len(record.pass_list) > 0:
                    of.write(f"\n# The following {len(record.pass_list)} checkpoints passed:\n")
                    for item in record.pass_list:
                        of.write(f"\t{item}\n")

                if len(record.fail_list) > 0:
                    of.write(f"\n# The following {len(record.fail_list)} checkpoints failed:\n")
                    for item in record.fail_list:
                        of.write(f"\t{item}\n")

                of.write("\n\n")

        logging.info(f"Generated report file '{outfile}'")
        if self.verbose:
            print(f"Generated report file '{outfile}'")
