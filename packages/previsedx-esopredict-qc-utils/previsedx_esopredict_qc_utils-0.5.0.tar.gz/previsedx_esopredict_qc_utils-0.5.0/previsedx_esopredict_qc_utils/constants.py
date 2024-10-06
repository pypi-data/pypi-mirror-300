import logging
import os

from datetime import datetime

DEFAULT_PROJECT = "esopredict-qc-utils"

DEFAULT_TIMESTAMP = str(datetime.today().strftime("%Y-%m-%d-%H%M%S"))

DEFAULT_OUTDIR = os.path.join(
    "/tmp/",
    os.getenv("USER"),
    DEFAULT_PROJECT,
    os.path.basename(__file__),
    DEFAULT_TIMESTAMP,
)

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False

DEFAULT_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "conf", "config.yaml"
)

GENE_NAMES = ["ACTIN", "FBN1", "HPP1", "P16", "RUNX3"]

# This is the default Excel worksheet name from
# which the data records will be retrieved/parsed.
# The software will first attempt to derive this value
# from the configuration file.
DEFAULT_RESULTS_SHEET_NAME = "Results"

# This is the default row number in the Results worksheet
# where the header row appears (0 based index).
# The software will first attempt to derive this value
# from the configuration file.
DEFAULT_HEADER_ROW_NUMBER = 42

# This is the default row where the first data record
# appears in the in the Results worksheet (0 based index).
# The software will first attempt to derive this value
# from the configuration file.
DEFAULT_FIRST_ROW_NUMBER = 43

# This is the default row where the last data record
# appears in the in the Results worksheet (0 based index).
# The software will first attempt to derive this value
# from the configuration file.
DEFAULT_LAST_ROW_NUMBER = 79


INTERMEDIATE_FILE_START_RECORD_LINE_NUMBER = 2

INTERMEDIATE_FILE_SAMPLE_ID_INDEX = 0
INTERMEDIATE_FILE_ACTIN_HPP1_INDEX = 1
INTERMEDIATE_FILE_HPP1_INDEX = 2
INTERMEDIATE_FILE_ACTIN_P16_INDEX = 3
INTERMEDIATE_FILE_P16_INDEX = 4
INTERMEDIATE_FILE_ACTIN_RUNX3_INDEX = 5
INTERMEDIATE_FILE_RUNX3_INDEX = 6
INTERMEDIATE_FILE_ACTIN_FBN1_INDEX = 7
INTERMEDIATE_FILE_FBN1_INDEX = 8
INTERMEDIATE_FILE_HPP1_FLAG_INDEX = 9
INTERMEDIATE_FILE_P16_FLAG_INDEX = 10
INTERMEDIATE_FILE_RUNX3_FLAG_INDEX = 11
INTERMEDIATE_FILE_FBN1_FLAG_INDEX = 12
INTERMEDIATE_FILE_HPP1_NMV_INDEX = 13
INTERMEDIATE_FILE_P16_NMV_INDEX = 14
INTERMEDIATE_FILE_RUNX3_NMV_INDEX = 15
INTERMEDIATE_FILE_FBN1_NMV_INDEX = 16
INTERMEDIATE_FILE_HPP1_FBN1_NMV_INDEX = 17
INTERMEDIATE_FILE_TRUNC_P16_NMV_INDEX = 18
INTERMEDIATE_FILE_COVARIATE_INDEX = 19
INTERMEDIATE_FILE_AGE_AT_BIOPSY_INDEX = 20
INTERMEDIATE_FILE_TRANS_HPP1_FBN1_NMV_INDEX = 21
INTERMEDIATE_FILE_TRANS_P16_NMV_INDEX = 22
INTERMEDIATE_FILE_TRANS_RUNX3_NMV_INDEX = 23
INTERMEDIATE_FILE_LP_INDEX = 24
INTERMEDIATE_FILE_NORMALIZED_PROGNOSTIC_SCORE_INDEX = 25
INTERMEDIATE_FILE_PREDICTED_RISK_CATEGORY_INDEX = 26
INTERMEDIATE_FILE_5_YR_PROGRESSION_RISK_INDEX = 27
INTERMEDIATE_FILE_5_YR_PROGRESSION_RISK_CI_LOW_INDEX = 28
INTERMEDIATE_FILE_5_YR_PROGRESSION_RISK_CI_HIGH_INDEX = 29

# If the write_intermediate_tab_delimited_file_validation_report is
# not defined or set in the conf/config.yaml configuration file, then
# if the following is set to True, then the validation report
# for the intermediate tab-delimited file parser will be written.
DEFAULT_WRITE_INTERMEDIATE_TAB_DELIMITED_FILE_VALIDATION_REPORT = False
