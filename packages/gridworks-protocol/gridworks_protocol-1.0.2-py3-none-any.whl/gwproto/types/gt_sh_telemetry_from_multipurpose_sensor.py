"""Type gt.sh.telemetry.from.multipurpose.sensor, version 100"""

from typing import List, Literal, Self

from pydantic import BaseModel, model_validator

from gwproto.enums import TelemetryName
from gwproto.property_format import SpaceheatName, UTCMilliseconds


class GtShTelemetryFromMultipurposeSensor(BaseModel):
    ScadaReadTimeUnixMs: UTCMilliseconds
    AboutNodeAliasList: list[SpaceheatName]
    TelemetryNameList: List[TelemetryName]
    ValueList: List[int]
    TypeName: Literal["gt.sh.telemetry.from.multipurpose.sensor"] = (
        "gt.sh.telemetry.from.multipurpose.sensor"
    )
    Version: Literal["100"] = "100"

    @model_validator(mode="after")
    def check_axiom_1(self) -> Self:
        """
        Axiom 1: ListLengthConsistency.
        AboutNodeAliasList, ValueList and TelemetryNameList must all have the same length.
        """
        if not (
            len(self.ValueList)
            == len(self.AboutNodeAliasList)
            == len(self.TelemetryNameList)
        ):
            raise ValueError(
                "Axiom 1: AboutNodeAliasList, ValueList and TelemetryNameList must all have the same length."
            )
        return self
