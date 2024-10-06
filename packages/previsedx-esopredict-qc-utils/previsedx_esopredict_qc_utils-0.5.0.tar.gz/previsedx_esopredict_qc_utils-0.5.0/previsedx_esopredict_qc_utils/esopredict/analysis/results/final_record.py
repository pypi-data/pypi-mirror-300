from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator


class FinalRecord(BaseModel):
    sample_id: Optional[str] = Field(
        None, description="The sample identifier (column A)"
    )

    actin_hpp1: Union[float, str] = Field("ND", description="The quantity of the Actin corresponding with the HPP1 gene")

    hpp1: Optional[float] = Field(None, description="The quantity of the HPP1 gene")

    actin_p16: Union[float, str] = Field("ND", description="The quantity of the Actin corresponding with the P16 gene")

    p16: Optional[float] = Field(None, description="The quantity of the P16 gene")

    actin_runx3: Union[float, str] = Field("ND", description="The quantity of the Actin corresponding with the RUNX3 gene")

    runx3: Optional[float] = Field(None, description="The quantity of the RUNX3 gene")

    actin_fbn1: Union[float, str] = Field("ND", description="The quantity of the Actin corresponding with the FBN1 gene")

    fbn1: Optional[str] = Field(None, description="The quantity of the FBN1 gene")

    hpp1_flag: Optional[float] = Field(None, description="The HPP1 flag (column L)")

    p16_flag: Optional[float] = Field(None, description="The P16 flag (column M)")

    runx3_flag: Optional[float] = Field(None, description="The RUNX3 flag (column N)")

    fbn1_flag: Optional[float] = Field(None, description="The FBN1 flag (column O)")

    hpp1_nmv: Optional[float] = Field(
        None, description="The HPP1 normalized methylated value (column P)"
    )

    p16_nmv: Optional[float] = Field(
        None, description="The P16 normalized methylated value (column Q)"
    )

    runx3_nmv: Optional[float] = Field(
        None, description="The RUNX3 normalized methylated value (column R)"
    )

    fbn1_nmv: Optional[float] = Field(
        None, description="The FBN1 normalized methylated value (column S)"
    )

    hpp1_fbn1_nmv: Optional[float] = Field(
        None,
        description="The ratio of HPP1 to FBN1 normalized methylated values (column T)",
    )

    trunc_p16_nmv: Optional[float] = Field(
        None, description="The trunc_P16_NMV (value <0.25=0.25) (column U)"
    )

    covariate: Optional[int] = Field(None, description="The covariate (column W)")

    age_at_biopsy: Optional[float] = Field(
        None, description="The age at biopsy (column X)"
    )

    trans_hpp1_fbn1_nmv: Optional[float] = Field(
        None,
        description="The square root of the ratio of HPP1 to FBN1 normalized methylated values (column X)",
    )

    trans_p16_nmv: Optional[float] = Field(
        None, description="The square root of the trunc_p16_nmv (column Y)"
    )

    trans_runx3_nmv: Optional[float] = Field(
        None,
        description="The square root of the RUNX3 normalized methylated value (column Z)",
    )

    lp: Optional[float] = Field(None, description="TBD")

    normalized_prognostic_score: Union[float, str] = Field("ND", description="The normalized prognostic score (column AB)")

    predicted_risk_category: Optional[str] = Field(
        "ND", description="The predicted risk category (column AC)"
    )

    five_year_progression_risk: Union[float, str] = Field("ND", description="The five year progression risk (column AD)")

    five_year_progression_risk_ci_low: Union[float, str] = Field("ND", description="The five year progression risk CI low (column AE)")

    five_year_progression_risk_ci_high: Union[float, str] = Field("ND", description="The five year progression risk CI high (column AF)")

    # Add support to convert percentage strings to floats
    @field_validator("five_year_progression_risk")
    def string_to_float_five_year_progression_risk(cls, v):
        if isinstance(v, str) and v.upper() == "ND":
            return "ND"
        if isinstance(v, str) and v.endswith("%"):
            v = v.replace("%", "")
            v = float(v) / 100
            return v
        return v

    @field_validator("five_year_progression_risk_ci_low")
    def string_to_float_five_year_progression_risk_ci_low(cls, v):
        if isinstance(v, str) and v.upper() == "ND":
            return "ND"
        if isinstance(v, str) and v.endswith("%"):
            v = v.replace("%", "")
            v = float(v) / 100
            return v
        return v

    @field_validator("five_year_progression_risk_ci_high")
    def string_to_float_five_year_progression_risk_ci_high(cls, v):
        if isinstance(v, str) and v.upper() == "ND":
            return "ND"
        if isinstance(v, str) and v.endswith("%"):
            v = v.replace("%", "")
            v = float(v) / 100
            return v
        return v
