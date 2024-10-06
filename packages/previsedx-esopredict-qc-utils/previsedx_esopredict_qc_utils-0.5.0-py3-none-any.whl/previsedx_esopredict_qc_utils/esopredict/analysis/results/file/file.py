from typing import Optional

import pydantic


class File(pydantic.BaseModel):
    run_id: Optional[str] = pydantic.Field(
        default=None,
        description="The run identifier",
    )

    analysis_date: Optional[str] = pydantic.Field(
        default=None,
        description="The date of the analysis",
    )

    analysis_id: Optional[str] = pydantic.Field(
        default=None,
        description="The analysis identifier",
    )

    lab_tech_initials: Optional[str] = pydantic.Field(
        default=None,
        description="The initials of the lab technician",
    )

    gene: Optional[str] = pydantic.Field(
        default=None,
        description="The gene being analyzed",
    )

    path: str = pydantic.Field(
        default=None,
        description="The path to the file",
    )

    basename: str = pydantic.Field(
        default=None,
        description="The basename of the file",
    )

    def __str__(self):
        return f"""File(
        analysis_date={self.analysis_date}
        analysis_id={self.analysis_id}
        basename={self.basename}
        gene={self.gene}
        lab_tech_initials={self.lab_tech_initials}
        path={self.path}
        run_id={self.run_id}
        )"""
