"""Type gt.sh.multipurpose.telemetry.status, version 100"""

from typing import Literal, Self

from pydantic import BaseModel, Field, model_validator

from gwproto.enums.telemetry_name import TelemetryName
from gwproto.property_format import (
    SpaceheatName,
    UTCMilliseconds,
)


class GtShMultipurposeTelemetryStatus(BaseModel):
    """
    Data read from a MultipurposeSensor run by a Spaceheat SCADA.

    A list of readings about a specific SpaceheatNode made by a MultipurposeSensor node, for
    a Spaceheat SCADA. Designed as part of a status message sent from the SCADA to its AtomicTNode
    typically once every 5 minutes. The nth element of each of its two lists refer to the same
    reading (i.e. what the value is, when it was read).

    [More info](https://gridworks-protocol.readthedocs.io/en/latest/multipurpose-sensor.html)
    """

    AboutNodeAlias: SpaceheatName = Field(
        description=(
            "The SpaceheatNode representing the physical object that the sensor reading is collecting "
            "data about. For example, a multipurpose temp sensor that reads 12 temperatures would "
            "have data for 12 different AboutNodeAliases, including say `a.tank1.temp1` for a "
            "temp sensor at the top of a water tank."
            "[More info](https://gridworks-protocol.readthedocs.io/en/latest/spaceheat-node.html)"
        ),
    )
    SensorNodeAlias: SpaceheatName
    TelemetryName: TelemetryName
    ValueList: list[int]
    ReadTimeUnixMsList: list[UTCMilliseconds]
    TypeName: Literal["gt.sh.multipurpose.telemetry.status"] = (
        "gt.sh.multipurpose.telemetry.status"
    )
    Version: Literal["101"] = "101"

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
