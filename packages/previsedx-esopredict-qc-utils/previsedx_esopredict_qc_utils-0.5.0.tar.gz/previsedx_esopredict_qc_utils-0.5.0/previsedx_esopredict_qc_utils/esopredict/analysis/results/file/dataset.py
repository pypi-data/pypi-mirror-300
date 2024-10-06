from typing import Any, Dict, List, Optional

import pydantic

from previsedx_esopredict_qc_utils.esopredict.analysis.results.file.file import File as ResultsFile


class Dataset(pydantic.BaseModel):
    # actin_file: str = pydantic.Field(..., description="The ACTIN file", frozen=True)
    # hpp1_file: str = pydantic.Field(..., description="The HPP1 file", frozen=True)
    # p16_file: str = pydantic.Field(..., description="The P16 file", frozen=True)
    # fbn1_file: str = pydantic.Field(..., description="The FBN1 file", frozen=True)
    # runx3_file: str = pydantic.Field(..., description="The RUNX3 file", frozen=True)

    def __init__(self, **data: Any):
        super().__init__(**data)
        # Add your custom initialization logic here
        self._run_id_list = None
        self._gene_to_run_id_lookup = {}

    run_id: str = pydantic.Field(
        ...,
        description="The run ID",
    )

    indir: Optional[str] = pydantic.Field(
        default=None,
        description="The input directory",
    )

    actin_file_count: Optional[int] = pydantic.Field(
        default=0,
        description="The number of ACTIN files",
    )

    hpp1_file_count: Optional[int] = pydantic.Field(
        default=0,
        description="The number of HPP1 files",
    )

    fbn1_file_count: Optional[int] = pydantic.Field(
        default=0,
        description="The number of FBN1 files",
    )

    p16_file_count: Optional[int] = pydantic.Field(
        default=0,
        description="The number of P16 files",
    )

    runx3_file_count: Optional[int] = pydantic.Field(
        default=0,
        description="The number of RUNX3 files",
    )

    run_id_to_actin_file_lookup: Optional[Dict[str, ResultsFile]] = pydantic.Field(
        default={},
        description="The lookup of run_id to ACTIN file",
    )

    run_id_to_fbn1_file_lookup: Optional[Dict[str, ResultsFile]] = pydantic.Field(
        default={},
        description="The lookup of run_id to FBN1 file",
    )

    run_id_to_hpp1_file_lookup: Optional[Dict[str, ResultsFile]] = pydantic.Field(
        default={},
        description="The lookup of run_id to HPP1 file",
    )

    run_id_to_p16_file_lookup: Optional[Dict[str, ResultsFile]] = pydantic.Field(
        default={},
        description="The lookup of run_id to P16 file",
    )

    run_id_to_runx3_file_lookup: Optional[Dict[str, ResultsFile]] = pydantic.Field(
        default={},
        description="The lookup of run_id to RUNX3 file",
    )

    def get_run_ids(self) -> List[str]:
        """Compile the list of run ID values.

        Returns:
            List[str]: The list of run ID values.
        """
        if self._run_id_list is None:
            self._run_id_list = []

            for run_id in self.run_id_to_actin_file_lookup.keys():
                self._run_id_list.append(run_id)
            for run_id in self.run_id_to_fbn1_file_lookup.keys():
                self._run_id_list.append(run_id)
                self._gene_to_run_id_lookup['FBN1'] = run_id
            for run_id in self.run_id_to_hpp1_file_lookup.keys():
                self._run_id_list.append(run_id)
                self._gene_to_run_id_lookup['HPP1'] = run_id
            for run_id in self.run_id_to_p16_file_lookup.keys():
                self._run_id_list.append(run_id)
                self._gene_to_run_id_lookup['P16'] = run_id
            for run_id in self.run_id_to_runx3_file_lookup.keys():
                self._run_id_list.append(run_id)
                self._gene_to_run_id_lookup['RUNX3'] = run_id

        # Derive the unique list of run_id values.
        self._run_id_list = list(set(self._run_id_list))

        return self._run_id_list

    def get_gene_to_run_id_lookup(self) -> Dict[str, str]:
        """Compile the lookup of gene to run ID values.

        Returns:
            Dict[str, str]: The lookup of gene to run ID values.
        """
        if not self._gene_to_run_id_lookup:
            self.get_run_ids()

        return self._gene_to_run_id_lookup
