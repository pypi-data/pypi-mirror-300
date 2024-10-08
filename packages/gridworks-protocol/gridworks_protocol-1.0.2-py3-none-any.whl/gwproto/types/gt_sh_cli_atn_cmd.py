"""Type gt.sh.cli.atn.cmd, version 110"""

from typing import Literal

from pydantic import BaseModel, Field

from gwproto.property_format import LeftRightDotStr, UUID4Str


class GtShCliAtnCmd(BaseModel):
    """
    AtomicTNode CLI Command.

    This is a generic type mechanism for a crude command line interface on a SCADA, brokered
    by the AtomicTNode.
    """

    FromGNodeAlias: LeftRightDotStr
    SendSnapshot: bool = Field(
        title="Send Snapshot",
        description=(
            "Asks SCADA to send back a snapshot. For this version of the type, nothing would "
            "happen if SendSnapshot were set to False. However, we include this in case additional "
            "variations are added later."
        ),
    )
    FromGNodeId: UUID4Str
    TypeName: Literal["gt.sh.cli.atn.cmd"] = "gt.sh.cli.atn.cmd"
    Version: Literal["110"] = "110"
