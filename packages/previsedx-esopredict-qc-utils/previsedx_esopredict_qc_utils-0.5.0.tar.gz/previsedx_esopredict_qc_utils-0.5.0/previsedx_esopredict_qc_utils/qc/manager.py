import logging
import os

import pandas as pd
from typing import List


from previsedx_esopredict_qc_utils import constants
from previsedx_esopredict_qc_utils.qc.auditor import Auditor
from previsedx_esopredict_qc_utils.qc.reporter import Reporter
from previsedx_esopredict_qc_utils.qc.record import Record
from previsedx_esopredict_qc_utils.esopredict.analysis.results.file.helper import Helper
from previsedx_esopredict_qc_utils.esopredict.analysis.results.intermediate.file.tsv.parser import Parser


class Manager:
    """Class for auditing the QC checks for esopredict."""

    def __init__(self, **kwargs):
        """Constructor for Manager"""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.indir = kwargs.get("indir", None)
        self.infile = kwargs.get("infile", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self.actin_file = None
        self.fbn1_file = None
        self.hpp1_file = None
        self.p16_file = None
        self.runx3_file = None
        self.gene_files = []
        self.run_id_list = None

        self.helper = Helper(**kwargs)
        self.auditor = Auditor(**kwargs)
        self.reporter = Reporter(**kwargs)

        self.intermediate_file_records = None

        logging.info(f"Instantiated Manager in file '{os.path.abspath(__file__)}'")

    def _load_dataset_files(self) -> None:
        self.dataset = self.helper.get_dataset()
        self.run_id_list = self.dataset.get_run_ids()

        for run_id in self.run_id_list:
            logging.info(f"Found run_id {run_id}")
            if run_id in self.dataset.run_id_to_actin_file_lookup:
                self.actin_file = self.dataset.run_id_to_actin_file_lookup.get(run_id)
                self.gene_files.append(self.actin_file)
                logging.info(f"Found ACTIN file {self.actin_file}")
            else:
                logging.error(f"Could not find ACTIN file for run_id {run_id}")

            if run_id in self.dataset.run_id_to_fbn1_file_lookup:
                self.fbn1_file = self.dataset.run_id_to_fbn1_file_lookup.get(run_id)
                self.gene_files.append(self.fbn1_file)
                logging.info(f"Found FBN1 file {self.fbn1_file}")
            else:
                logging.error(f"Could not find FBN1 file for run_id {run_id}")

            if run_id in self.dataset.run_id_to_hpp1_file_lookup:
                self.hpp1_file = self.dataset.run_id_to_hpp1_file_lookup.get(run_id)
                self.gene_files.append(self.hpp1_file)
                logging.info(f"Found HPP1 file {self.hpp1_file}")
            else:
                logging.error(f"Could not find HPP1 file for run_id {run_id}")

            if run_id in self.dataset.run_id_to_p16_file_lookup:
                self.p16_file = self.dataset.run_id_to_p16_file_lookup.get(run_id)
                self.gene_files.append(self.p16_file)
                logging.info(f"Found P16 file {self.p16_file}")
            else:
                logging.error(f"Could not find P16 file for run_id {run_id}")

            if run_id in self.dataset.run_id_to_runx3_file_lookup:
                self.runx3_file = self.dataset.run_id_to_runx3_file_lookup.get(run_id)
                self.gene_files.append(self.runx3_file)
                logging.info(f"Found RUNX3 file {self.runx3_file}")
            else:
                logging.error(f"Could not find RUNX3 file for run_id {run_id}")

    def run_qc_checks(self) -> None:
        logging.info("Will perform all QC checks")

        self._run_pre_report_generation_qc_checks()

        self._run_post_report_generation_qc_checks()

        self.reporter.generate_report(records=self.auditor.get_records())

    def _run_pre_report_generation_qc_checks(self) -> None:
        """Run QC checks on the gene files."""
        logging.info("Will perform all pre-report QC checks")

        self._load_dataset_files()

        self._run_standard_curve_checks()

        self._run_dilution_for_standards_checks()

    def _run_post_report_generation_qc_checks(self) -> None:
        """Run QC checks on the esopredict generated intermediate tab-delimited file."""
        logging.info("Will perform all post-report QC checks")

        self._load_intermediate_file_records()
        self._run_neg_checks()
        self._run_ntc_checks()
        self._run_ext_checks()
        self._run_pos_high_checks()
        self._run_sample_qc_beta_actin_checks()

    def _load_intermediate_file_records(self) -> None:
        """Parse the esopredict generated intermediate tab-delimited file."""
        logging.info("Will attempt to load records from the intermediate tab-delimited file")

        parser = Parser(
            config=self.config,
            config_file=self.config_file,
            logfile=self.logfile,
            outdir=self.outdir,
            verbose=self.verbose,
        )
        self.intermediate_file_records = parser.get_records(self.infile)

    def _get_audit_record(self, id: str) -> Record:
        """Create an audit record.

        Args:
            id (str): The ID of the check.

        Returns:
            Record: The audit record.
        """
        desc = self.config.get("checks").get(id).get("desc")

        name = self.config.get("checks").get(id).get("name")

        record = Record(
            id=id,
            name=name,
            desc=desc,
        )

        return record

    def _run_standard_curve_checks(self, check_id: str = "standard_curve_checks") -> None:
        """Perform the Standard Curve QC checks.

        Args:
            check_id (str): The ID of the check.
        """
        logging.info("Will perform QC checks for standard curve")

        efficiency_min_threshold = self.config.get("checks").get("efficiency_threshold").get("min")
        efficiency_max_threshold = self.config.get("checks").get("efficiency_threshold").get("max")
        r_squared = self.config.get("checks").get("r_squared")

        pass_list = []
        fail_list = []

        r_squared_lookup = {}
        efficiency_lookup = {}

        error_ctr = 0

        for gene_file in self.gene_files:
            logging.info(f"Processing gene file '{gene_file.basename}'")
            records = self.helper.get_gene_file_records(gene_file)
            for record in records:
                if not record.rsuperscript2 > r_squared:
                    logging.error(f"R-squared value '{record.rsuperscript2}' is not greater than {r_squared} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                    fail_list.append(f"R-squared value '{record.rsuperscript2}' is not greater than {r_squared} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                    error_ctr += 1
                else:
                    if record.rsuperscript2 not in r_squared_lookup:
                        r_squared_lookup[record.rsuperscript2] = True
                        logging.info(f"R-squared value '{record.rsuperscript2}' is greater than {r_squared} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        pass_list.append(f"R-squared value '{record.rsuperscript2}' is greater than {r_squared} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")

                if efficiency_min_threshold < record.efficiency < efficiency_max_threshold:
                    if record.efficiency not in efficiency_lookup:
                        efficiency_lookup[record.efficiency] = True
                        logging.info(f"Efficiency value '{record.efficiency}' is within the range of {efficiency_min_threshold} to {efficiency_max_threshold} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        pass_list.append(f"Efficiency value '{record.efficiency}' is within the range of {efficiency_min_threshold} to {efficiency_max_threshold} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                else:
                    logging.error(f"Efficiency value '{record.efficiency}' is not within the range of {efficiency_min_threshold} to {efficiency_max_threshold} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                    fail_list.append(f"Efficiency value '{record.efficiency}' is not within the range of {efficiency_min_threshold} to {efficiency_max_threshold} for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                    error_ctr += 1

        record = self._get_audit_record(check_id)
        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)

    def _run_neg_checks(self, check_id: str = "neg_checks") -> None:
        logging.info("Will perform QC checks for NEG records")

        pass_list = []
        fail_list = []

        error_ctr = 0

        for record in self.intermediate_file_records:

            if record.sample_id.upper().startswith("NEG"):
                # TODO: Ask Lisa abou EXT-NEG

                # Check the NMV percentages

                if not self._check_nmv_percentage_not_defined(
                    record.hpp1_nmv,
                    record.sample_id,
                    "HPP1_NMV",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._check_nmv_percentage_not_defined(
                    record.runx3_nmv,
                    record.sample_id,
                    "RUNX3_NMV",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._check_nmv_percentage_not_defined(
                    record.fbn1_nmv,
                    record.sample_id,
                    "FBN1_NMV",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                p16_nmv_converted = record.p16_nmv * 100
                p16_nmv_converted = round(p16_nmv_converted, 4)

                if p16_nmv_converted < 1.000:
                    logging.info(f"P16_NMV value '{p16_nmv_converted}' is less than 1.000 for sample '{record.sample_id}' in the intermediate tab-delimited file")
                    pass_list.append(f"P16_NMV value '{p16_nmv_converted}' is less than 1.000 for sample '{record.sample_id}' in the intermediate tab-delimited file")
                else:
                    logging.error(f"P16_NMV value '{p16_nmv_converted}' is NOT less than 1.000 for sample '{record.sample_id}' in the intermediate tab-delimited file")
                    fail_list.append(f"P16_NMV value '{p16_nmv_converted}' is less than 1.000 for sample '{record.sample_id}' in the intermediate tab-delimited file")
                    error_ctr += 1

                # Check the Beta-ACTIN quantities

                if not self._is_beta_actin_quantity_pass(
                    record.actin_hpp1,
                    record.sample_id,
                    "ACTIN_HPP1",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._is_beta_actin_quantity_pass(
                    record.actin_fbn1,
                    record.sample_id,
                    "ACTIN_FBN1",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._is_beta_actin_quantity_pass(
                    record.actin_runx3,
                    record.sample_id,
                    "ACTIN_RUNX3",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._is_beta_actin_quantity_pass(
                    record.actin_p16,
                    record.sample_id,
                    "ACTIN_P16",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

        record = self._get_audit_record(check_id)
        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)

    def _check_nmv_percentage_not_defined(
        self,
        value: float,
        sample_id: str,
        nmv_name: str,
        pass_list: List[str],
        fail_list: List[str],
    ) -> bool:
        """Check whether the NMV percentage is not defined.

        Args:
            value (float): The value to check.
            sample_id (str): The sample ID.
            nmv_name (str): The name of the NMV.
            pass_list (List[str]): The list of passed checks.
            fail_list (List[str]): The list of failed checks.

        Returns:
            bool: True if the value is empty or 'ND' or 0, False otherwise.
        """
        if (value is None or pd.isna(value)) or value == 0:
            logging.info(f"{nmv_name} value {value} is empty or 'ND' or 0 for sample '{sample_id}' in the intermediate tab-delimited file")
            pass_list.append(f"{nmv_name} value {value} is empty or 'ND' or 0 for sample '{sample_id}' in the intermediate tab-delimited file")
            return True
        else:
            logging.error(f"{nmv_name} value '{value}' should be empty or 'ND' or 0 for sample '{sample_id}' in the intermediate tab-delimited file")
            fail_list.append(f"{nmv_name} value '{value}' should be empty or 'ND' or 0 for sample '{sample_id}' in the intermediate tab-delimited file")
            return False

    def _is_beta_actin_quantity_pass(
        self,
        value: float,
        sample_id: str,
        beta_actin_name: str,
        pass_list: List[str],
        fail_list: List[str],
        min_value: float = 0.0016,
        max_value: float = 1.000,
    ) -> bool:
        """Check whether the Beta-ACTIN value is between 0.0016 and 1.000.

        Args:
            value (float): The value to check.
            sample_id (str): The sample ID.
            beta_actin_name (str): The name of the beta-actin gene.
            pass_list (List[str]): The list of passed checks.
            fail_list (List[str]): The list of failed checks.
            min_value (float): The minimum value.
            max_value (float): The maximum value.

        Returns:
            bool: True if the value is between 0.0016 and 1.000, False otherwise.
        """
        if min_value < value < max_value:
            logging.info(f"{beta_actin_name} value {value} is between {min_value} and {max_value} for sample '{sample_id}' in the intermediate tab-delimited file")
            pass_list.append(f"{beta_actin_name} value {value} is between {min_value} and {max_value} for sample '{sample_id}' in the intermediate tab-delimited file")
            return True
        else:
            logging.error(f"{beta_actin_name} value '{value}' should be between {min_value} and {max_value} for sample '{sample_id}' in the intermediate tab-delimited file")
            fail_list.append(f"{beta_actin_name} value '{value}' should be between {min_value} and {max_value} for sample '{sample_id}' in the intermediate tab-delimited file")
            return False

    def _is_beta_actin_quantity_not_defined(
        self,
        value: float,
        sample_id: str,
        beta_actin_name: str,
        pass_list: List[str],
        fail_list: List[str],
    ) -> bool:
        """Verify that the Beta-ACTIN quantity is not defined.

        Args:
            value (float): The value to check.
            sample_id (str): The sample ID.
            beta_actin_name (str): The name of the Beta-ACTIN.
            pass_list (List[str]): The list of passed checks.
            fail_list (List[str]): The list of failed checks.

        Returns:
            bool: True if the value is empty or 'ND' or 0, False otherwise.
        """
        if (value is None or pd.isna(value)) or value == 0 or value == "ND":
            logging.info(f"{beta_actin_name} value {value} is empty or 'ND' or 0 for sample '{sample_id}' in the intermediate tab-delimited file")
            pass_list.append(f"{beta_actin_name} value {value} is empty or 'ND' or 0 for sample '{sample_id}' in the intermediate tab-delimited file")
            return True
        else:
            logging.error(f"{beta_actin_name} value '{value}' should be empty or 'ND' or 0 for sample '{sample_id}' in the intermediate tab-delimited file")
            fail_list.append(f"{beta_actin_name} value '{value}' should be empty or 'ND' or 0 for sample '{sample_id}' in the intermediate tab-delimited file")
            return False

    def _run_ntc_checks(self, check_id: str = "ntc_checks") -> None:
        logging.info("Will perform QC checks for NTC records")

        pass_list = []
        fail_list = []

        error_ctr = 0

        for record in self.intermediate_file_records:

            if record.sample_id.upper().startswith("NTC"):
                # TODO: Ask Lisa abou EXT-NEG

                # Check the NMV percentages

                if not self._check_nmv_percentage_not_defined(
                    record.hpp1_nmv,
                    record.sample_id,
                    "HPP1_NMV",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._check_nmv_percentage_not_defined(
                    record.runx3_nmv,
                    record.sample_id,
                    "RUNX3_NMV",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._check_nmv_percentage_not_defined(
                    record.fbn1_nmv,
                    record.sample_id,
                    "FBN1_NMV",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._check_nmv_percentage_not_defined(
                    record.p16_nmv,
                    record.sample_id,
                    "P16_NMV",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                # Check the Beta-ACTIN quantities

                if not self._is_beta_actin_quantity_not_defined(
                    record.actin_hpp1,
                    record.sample_id,
                    "ACTIN_HPP1",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._is_beta_actin_quantity_not_defined(
                    record.actin_fbn1,
                    record.sample_id,
                    "ACTIN_FBN1",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._is_beta_actin_quantity_not_defined(
                    record.actin_runx3,
                    record.sample_id,
                    "ACTIN_RUNX3",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._is_beta_actin_quantity_not_defined(
                    record.actin_p16,
                    record.sample_id,
                    "ACTIN_P16",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

        record = self._get_audit_record(check_id)
        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)

    def _run_ext_checks(self, check_id: str = "ext_checks") -> None:
        logging.info("Will perform QC checks for EXT records")

        pass_list = []
        fail_list = []

        error_ctr = 0

        for record in self.intermediate_file_records:

            logging.info(f"Processing intermediate final record with sample_id {record.sample_id}")

            if record.sample_id.upper().startswith("EXT"):

                # Check the NMV percentages

                if not self._check_nmv_percentage_not_defined(
                    record.hpp1_nmv,
                    record.sample_id,
                    "HPP1_NMV",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._check_nmv_percentage_not_defined(
                    record.runx3_nmv,
                    record.sample_id,
                    "RUNX3_NMV",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._check_nmv_percentage_not_defined(
                    record.fbn1_nmv,
                    record.sample_id,
                    "FBN1_NMV",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._check_nmv_percentage_not_defined(
                    record.p16_nmv,
                    record.sample_id,
                    "P16_NMV",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                # Check the Beta-ACTIN quantities

                if not self._is_beta_actin_quantity_not_defined(
                    record.actin_hpp1,
                    record.sample_id,
                    "ACTIN_HPP1",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._is_beta_actin_quantity_not_defined(
                    record.actin_fbn1,
                    record.sample_id,
                    "ACTIN_FBN1",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._is_beta_actin_quantity_not_defined(
                    record.actin_runx3,
                    record.sample_id,
                    "ACTIN_RUNX3",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

                if not self._is_beta_actin_quantity_not_defined(
                    record.actin_p16,
                    record.sample_id,
                    "ACTIN_P16",
                    pass_list,
                    fail_list,
                ):
                    error_ctr += 1

        record = self._get_audit_record(check_id)
        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)

    def _run_dilution_for_standards_checks(self, check_id: str = "dilution_for_standards_checks") -> None:
        """Perform dilution checks for standards.

        Review the five-point standard curve to ensure there are all five standards
        labeled as Standards in the Quantstudio software.  All other sampels should be labeled as
        unknown.  Check the values for the standard curve:

            Standard 1 = 1 in wells A11, A12

            1:5 = 0.2 in wells B11, B12

            1:25 = 0.04 in wells C11, C12

            1:125 = 0.008 in wells D11, D12

            1:625 = 0.0016 in wells E11, E12

        Args:
            check_id (str): The ID of the check.
        """
        logging.info("Will perform QC checks for dilution of standards")

        # Standard curve checks
        # Curve QC
        # Check 1 standard curve
        # R-squared value

        pass_list = []
        fail_list = []

        error_ctr = 0
        good_ctr = 0
        total_standard_ctr = 0

        for gene_file in self.gene_files:

            gene_standard_ctr = 0
            std1_ctr = 0
            std2_ctr = 0
            std3_ctr = 0
            std4_ctr = 0
            std5_ctr = 0

            logging.info(f"Processing gene file '{gene_file.basename}'")
            records = self.helper.get_gene_file_records(gene_file)

            for record in records:
                if record.samplename.upper() == "STD 1" or record.samplename.upper() == "STD1":
                    std1_ctr += 1

                    if round(record.quantity, 3) == 1.000:
                        logging.info(f"Quantity value '{round(record.quantity, 3)}' is 1.000 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        pass_list.append(f"Quantity value '{round(record.quantity, 3)}' is 1.000 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        good_ctr += 1
                    else:
                        logging.error(f"Quantity value '{round(record.quantity, 3)}' is not 1.000 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        fail_list.append(f"Quantity value '{round(record.quantity, 3)}' is not 1.000 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        error_ctr += 1

                elif record.samplename.upper() == "STD 2" or record.samplename.upper() == "STD2":
                    std2_ctr += 1

                    if round(record.quantity, 3) == 0.200:
                        logging.info(f"Quantity value '{round(record.quantity, 3)}' is 0.200 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        pass_list.append(f"Quantity value '{round(record.quantity, 3)}' is 0.200 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        good_ctr += 1
                    else:
                        logging.error(f"Quantity value '{round(record.quantity, 3)}' is not 0.200 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        fail_list.append(f"Quantity value '{round(record.quantity, 3)}' is not 0.200 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        error_ctr += 1

                elif record.samplename.upper() == "STD 3" or record.samplename.upper() == "STD3":
                    std3_ctr += 1

                    if round(record.quantity, 3) == 0.040:
                        logging.info(f"Quantity value '{round(record.quantity, 3)}' is 0.040 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        pass_list.append(f"Quantity value '{round(record.quantity, 3)}' is 0.040 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        good_ctr += 1
                    else:
                        logging.error(f"Quantity value '{round(record.quantity, 3)}' is not 0.040 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        fail_list.append(f"Quantity value '{round(record.quantity, 3)}' is not 0.040 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        error_ctr += 1

                elif record.samplename.upper() == "STD 4" or record.samplename.upper() == "STD4":
                    std4_ctr += 1

                    if round(record.quantity, 3) == 0.008:
                        logging.info(f"Quantity value '{round(record.quantity, 3)}' is 0.008 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        pass_list.append(f"Quantity value '{round(record.quantity, 3)}' is 0.008 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        good_ctr += 1
                    else:
                        logging.error(f"Quantity value '{round(record.quantity, 3)}' is not 0.008 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        fail_list.append(f"Quantity value '{round(record.quantity, 3)}' is not 0.008 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        error_ctr += 1

                elif record.samplename.upper() == "STD 5" or record.samplename.upper() == "STD5":
                    std5_ctr += 1

                    if round(record.quantity, 4) == 0.0016:
                        logging.info(f"Quantity value '{round(record.quantity, 4)}' is 0.0016 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        pass_list.append(f"Quantity value '{round(record.quantity, 4)}' is 0.0016 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        good_ctr += 1
                    else:
                        logging.error(f"Quantity value '{round(record.quantity, 4)}' is not 0.0016 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        fail_list.append(f"Quantity value '{round(record.quantity, 4)}' is not 0.0016 for sample '{record.samplename}' in well position '{record.wellposition}' in gene file '{gene_file.basename}'")
                        error_ctr += 1

            gene_standard_ctr = std1_ctr + std2_ctr + std3_ctr + std4_ctr + std5_ctr

            # ------------------------------------------
            # Check number of standards STD1
            # ------------------------------------------
            if 1 <= std1_ctr <= 4:
                logging.info(f"Found {std1_ctr} STD1 standards in gene file '{gene_file.basename}'")
                pass_list.append(f"Found {std1_ctr} STD1 standards in gene file '{gene_file.basename}'")
            else:
                logging.error(f"Expected 1 or 2 STD1 standards in gene file '{gene_file.basename}', found {std1_ctr}")
                fail_list.append(f"Expected 1 or 2 STD1 standards in gene file '{gene_file.basename}', found {std1_ctr}")
                error_ctr += 1

            # ------------------------------------------
            # Check number of standards STD5
            # ------------------------------------------
            if 1 <= std5_ctr <= 4:
                logging.info(f"Found {std5_ctr} STD5 standards in gene file '{gene_file.basename}'")
                pass_list.append(f"Found {std5_ctr} STD5 standards in gene file '{gene_file.basename}'")
            else:
                logging.error(f"Expected 1 or 2 STD5 standards in gene file '{gene_file.basename}', found {std5_ctr}")
                fail_list.append(f"Expected 1 or 2 STD5 standards in gene file '{gene_file.basename}', found {std5_ctr}")
                error_ctr += 1

            if 18 <= gene_standard_ctr <= 20:
                logging.error(f"Expected between 8 and 10 standards in gene file '{gene_file.basename}', found {gene_standard_ctr}")
                fail_list.append(f"Expected between 8 and 10 standards in gene file '{gene_file.basename}', found {gene_standard_ctr}")
                error_ctr += 1
            else:
                logging.info(f"Found {gene_standard_ctr} standards in gene file '{gene_file.basename}'")
                pass_list.append(f"Found {gene_standard_ctr} standards in gene file '{gene_file.basename}'")

            total_standard_ctr += gene_standard_ctr

        if 40 <= total_standard_ctr <= 50:
            logging.info(f"Found {total_standard_ctr} standards among all gene files")
            pass_list.append(f"Found {total_standard_ctr} standards among all gene files")
        else:
            logging.error(f"Expected between 40 and 50 standards among all gene files, found {total_standard_ctr}")
            fail_list.append(f"Expected between 40 and 50 standards among all gene files, found {total_standard_ctr}")
            error_ctr += 1

        record = self._get_audit_record(check_id)
        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0 or good_ctr != 50:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)

    def _run_pos_high_checks(self, check_id: str = "pos_high_checks") -> None:
        """Perform checks on the intermediate tab-delimited file.

        Check the ACTIN value in the intermediate file to ensure it is greater than 0.0016.

        Args:
            check_id (str): The ID of the check.
        """
        logging.info("Will perform QC checks for POS-HIGH NMV values")

        hpp1_nmv_min_threshold = self.config.get("checks").get("nmv_thresholds").get("hpp1").get("min")
        hpp1_nmv_max_threshold = self.config.get("checks").get("nmv_thresholds").get("hpp1").get("max")

        fbn1_nmv_min_threshold = self.config.get("checks").get("nmv_thresholds").get("fbn1").get("min")
        fbn1_nmv_max_threshold = self.config.get("checks").get("nmv_thresholds").get("fbn1").get("max")

        p16_nmv_min_threshold = self.config.get("checks").get("nmv_thresholds").get("p16").get("min")
        p16_nmv_max_threshold = self.config.get("checks").get("nmv_thresholds").get("p16").get("max")

        runx3_nmv_min_threshold = self.config.get("checks").get("nmv_thresholds").get("runx3").get("min")
        runx3_nmv_max_threshold = self.config.get("checks").get("nmv_thresholds").get("runx3").get("max")

        error_ctr = 0

        pass_list = []
        fail_list = []

        for record in self.intermediate_file_records:

            if not record.sample_id.startswith("POS"):
                continue

            # Check the Beta-ACTIN quantities

            if not self._is_beta_actin_quantity_pass(
                record.actin_hpp1,
                record.sample_id,
                "ACTIN_HPP1",
                pass_list,
                fail_list,
            ):
                error_ctr += 1

            if not self._is_beta_actin_quantity_pass(
                record.actin_fbn1,
                record.sample_id,
                "ACTIN_FBN1",
                pass_list,
                fail_list,
            ):
                error_ctr += 1

            if not self._is_beta_actin_quantity_pass(
                record.actin_runx3,
                record.sample_id,
                "ACTIN_RUNX3",
                pass_list,
                fail_list,
            ):
                error_ctr += 1

            if not self._is_beta_actin_quantity_pass(
                record.actin_p16,
                record.sample_id,
                "ACTIN_P16",
                pass_list,
                fail_list,
            ):
                error_ctr += 1

            converted_hpp1_nmv = record.hpp1_nmv * 100
            converted_fbn1_nmv = record.fbn1_nmv * 100
            converted_p16_nmv = record.p16_nmv * 100
            converted_runx3_nmv = record.runx3_nmv * 100

            if not self._is_nmv_value_range_pass(
                record.sample_id,
                converted_hpp1_nmv,
                "HPP1_NMV",
                hpp1_nmv_min_threshold,
                hpp1_nmv_max_threshold,
                pass_list,
                fail_list,
            ):
                error_ctr += 1

            if not self._is_nmv_value_range_pass(
                record.sample_id,
                converted_fbn1_nmv,
                "FBN1_NMV",
                fbn1_nmv_min_threshold,
                fbn1_nmv_max_threshold,
                pass_list,
                fail_list,
            ):
                error_ctr += 1

            if not self._is_nmv_value_range_pass(
                record.sample_id,
                converted_p16_nmv,
                "P16_NMV",
                p16_nmv_min_threshold,
                p16_nmv_max_threshold,
                pass_list,
                fail_list,
            ):
                error_ctr += 1

            if not self._is_nmv_value_range_pass(
                record.sample_id,
                converted_runx3_nmv,
                "RUNX3_NMV",
                runx3_nmv_min_threshold,
                runx3_nmv_max_threshold,
                pass_list,
                fail_list,
            ):
                error_ctr += 1

        record = self._get_audit_record(check_id)
        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)

    def _is_nmv_value_range_pass(
        self,
        sample_id: str,
        value: float,
        nmv_name: str,
        min_value: float,
        max_value: float,
        pass_list: List[str],
        fail_list: List[str],
    ) -> bool:
        """Check whether the NMV value is within the range.

        Args:
            sample_id (str): The sample ID.
            value (float): The value to check.
            nmv_name (str): The name of the NMV.
            min_value (float): The minimum value.
            max_value (float): The maximum value.
            pass_list (List[str]): The list of passed checks.
            fail_list (List[str]): The list of failed checks.

        Returns:
            bool: True if the value is within the range, False otherwise.
        """
        if min_value < value < max_value:
            logging.info(f"{nmv_name} value '{value}' is within the range of {min_value} to {max_value} for sample '{sample_id}'")
            pass_list.append(f"{nmv_name} value '{value}' is within the range of {min_value} to {max_value} for sample '{sample_id}'")
            return True
        else:
            logging.error(f"{nmv_name} value '{value}' is not within the range of {min_value} to {max_value} for sample '{sample_id}'")
            fail_list.append(f"{nmv_name} value '{value}' is not within the range of {min_value} to {max_value} for sample '{sample_id}'")
            return False

    def _run_sample_qc_beta_actin_checks(
        self,
        check_id: str = "sample_qc_beta_actin_checks",
    ) -> None:
        """Perform checks on the intermediate tab-delimited file.

        Check the ACTIN value in the intermediate file to ensure it is greater than 0.0016.

        Args:
            check_id (str): The ID of the check.
            min_value (float): The minimum value.
            max_value (float): The maximum value.
        """
        logging.info("Will perform QC checks for Beta-ACTIN thresholds")

        actin_min_threshold = self.config.get("checks").get("actin_threshold").get("min")
        actin_max_threshold = self.config.get("checks").get("actin_threshold").get("max")

        error_ctr = 0

        pass_list = []
        fail_list = []

        for record in self.intermediate_file_records:

            logging.info(f"Processing record '{record}'")

            if record.sample_id.startswith("POS"):
                continue

            if record.sample_id.startswith("NEG"):
                continue

            if record.sample_id.startswith("NTC"):
                continue

            if record.sample_id.startswith("EXT"):
                continue

            if actin_min_threshold < record.actin_fbn1 < actin_max_threshold:
                logging.info(f"ACTIN FBN1 value '{record.actin_fbn1}' is between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"ACTIN FBN1 value '{record.actin_fbn1}' is between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"ACTIN FBN1 value '{record.actin_fbn1}' is not between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"ACTIN FBN1 value '{record.actin_fbn1}' is not between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

            if actin_min_threshold < record.actin_hpp1 < actin_max_threshold:
                logging.info(f"ACTIN HPP1 value '{record.actin_hpp1}' is between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"ACTIN HPP1 value '{record.actin_hpp1}' is between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"ACTIN HPP1 value '{record.actin_hpp1}' is not between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"ACTIN HPP1 value '{record.actin_hpp1}' is not between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

            if actin_min_threshold < record.actin_p16 < actin_max_threshold:
                logging.info(f"ACTIN P16 value '{record.actin_p16}' is between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"ACTIN P16 value '{record.actin_p16}' is between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"ACTIN P16 value '{record.actin_p16}' is not between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"ACTIN P16 value '{record.actin_p16}' is not between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

            if actin_min_threshold < record.actin_runx3 < actin_max_threshold:
                logging.info(f"ACTIN RUNX3 value '{record.actin_runx3}' is between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                pass_list.append(f"ACTIN RUNX3 value '{record.actin_runx3}' is between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
            else:
                logging.error(f"ACTIN RUNX3 value '{record.actin_runx3}' is not between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                fail_list.append(f"ACTIN RUNX3 value '{record.actin_runx3}' is not between {actin_min_threshold} and {actin_max_threshold} for sample '{record.sample_id}'")
                error_ctr += 1

        record = self._get_audit_record(check_id)

        record.pass_list = pass_list
        record.fail_list = fail_list

        if error_ctr > 0:
            record.status = "FAIL"
        else:
            record.status = "PASS"
        self.auditor.add_record(record)
