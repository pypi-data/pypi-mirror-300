"""Type gt.sh.simple.telemetry.status, version 100"""

from typing import List, Literal, Self

from pydantic import BaseModel, model_validator

from gwproto.enums.telemetry_name import TelemetryName
from gwproto.property_format import LeftRightDotStr, UTCMilliseconds


class GtShSimpleTelemetryStatus(BaseModel):
    """
    Data read from a SimpleSensor run by a SpaceHeat SCADA.

    A list of readings from a simple sensor for a Spaceheat SCADA. Designed as part of a status
    message sent from the SCADA to its AtomicTNode typically once every 5 minutes. The nth element
    of each of its two lists refer to the same reading (i.e. what the value is, when it was
    read).

    [More info](https://gridworks-protocol.readthedocs.io/en/latest/simple-sensor.html)
    """

    ShNodeAlias: LeftRightDotStr
    TelemetryName: TelemetryName
    ValueList: List[int]
    ReadTimeUnixMsList: List[UTCMilliseconds]
    TypeName: Literal["gt.sh.simple.telemetry.status"] = "gt.sh.simple.telemetry.status"
    Version: Literal["100"] = "100"

    @model_validator(mode="after")
    def check_axiom_1(self) -> Self:
        """
        Axiom 1: ListLengthConsistency.
        ValueList and ReadTimeUnixMsList must have the same length.
        """
        if len(self.ValueList) != len(self.ReadTimeUnixMsList):
            raise ValueError(
                "Axiom 1: ValueList and ReadTimeUnixMsList must have the same length."
            )
        return self

    def __hash__(self) -> int:
        return hash((type(self), *self.__dict__.values()))
