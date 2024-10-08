"""Type gt.sh.status, version 110"""

from typing import List, Literal

from pydantic import BaseModel

from gwproto.property_format import LeftRightDotStr, UTCSeconds, UUID4Str
from gwproto.types.gt_sh_booleanactuator_cmd_status import (
    GtShBooleanactuatorCmdStatus,
)
from gwproto.types.gt_sh_multipurpose_telemetry_status import (
    GtShMultipurposeTelemetryStatus,
)
from gwproto.types.gt_sh_simple_telemetry_status import (
    GtShSimpleTelemetryStatus,
)


class GtShStatus(BaseModel):
    """
    Status message sent by a Spaceheat SCADA every 5 minutes
    """

    FromGNodeAlias: LeftRightDotStr
    FromGNodeId: UUID4Str
    AboutGNodeAlias: LeftRightDotStr
    SlotStartUnixS: UTCSeconds
    ReportingPeriodS: int
    SimpleTelemetryList: list[GtShSimpleTelemetryStatus]
    MultipurposeTelemetryList: list[GtShMultipurposeTelemetryStatus]
    BooleanactuatorCmdList: List[GtShBooleanactuatorCmdStatus]
    StatusUid: UUID4Str
    TypeName: Literal["gt.sh.status"] = "gt.sh.status"
    Version: Literal["110"] = "110"

    def __hash__(self) -> int:
        return hash(self.StatusUid)
