import logging
import os

from typing import List
from previsedx_esopredict_qc_utils import constants
from previsedx_esopredict_qc_utils.qc.record import Record


class Auditor:
    """Class for auditing the QC checks for esopredict."""

    def __init__(self, **kwargs):
        """Constructor for Auditor"""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self._check_number = 0
        self._check_list = []
        logging.info(f"Instantiated Auditor in file '{os.path.abspath(__file__)}'")

    def add_record(self, record: Record) -> None:
        """Method to add a record to the QC checks.

        Args:
            record (Record): the record to be added to the list of checks.
        """
        self._check_number += 1

        record.number = self._check_number

        self._check_list.append(record)

        logging.info(f"Added record '{record.id}' with status '{record.status}'")

    def add_audit_record(self, id: str, status: str = "FAIL") -> None:
        """Method to add an audit record to the QC checks.

        Args:
            id (str): the ID of the check.
            status (str): the status of the check.
        """
        self._check_number += 1

        desc = self.config.get("checks").get(id).get("desc")

        name = self.config.get("checks").get(id).get("name")

        record = Record(
            id=id,
            status=status,
            name=name,
            desc=desc,
            number=self._check_number
        )

        self._check_list.append(record)

        logging.info(f"Added record '{record.id}' with status '{record.status}'")

    def get_records(self) -> List[Record]:
        """Method to get the list of records.

        Returns:
            List[Record]: the list of records.
        """
        return self._check_list
