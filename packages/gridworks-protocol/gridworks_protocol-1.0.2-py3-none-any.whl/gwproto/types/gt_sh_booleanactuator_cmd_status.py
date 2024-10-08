"""Type gt.sh.booleanactuator.cmd.status, version 100"""

from typing import Literal

from pydantic import BaseModel, Field

from gwproto.property_format import LeftRightDotStr


class GtShBooleanactuatorCmdStatus(BaseModel):
    """
    Boolean  Actuator Driver Command Status Package.

    This is a subtype of the status message sent from a SCADA to its AtomicTNode. It contains
    a list of all the commands that a particular boolean actuator actor has reported as sending
    as actuation commands to its driver in the last transmission period (typically 5 minutes).

    [More info](https://gridworks.readthedocs.io/en/latest/relay-state.html)
    """

    ShNodeAlias: LeftRightDotStr = Field(
        description=(
            "The alias of the spaceheat node that is getting actuated. For example, `a.elt1.relay` "
            "would likely indicate the relay for a resistive element."
            "[More info](https://gridworks-protocol.readthedocs.io/en/latest/boolean-actuator.html)"
        ),
    )
    RelayStateCommandList: list[bool]
    CommandTimeUnixMsList: list[int]
    TypeName: Literal["gt.sh.booleanactuator.cmd.status"] = (
        "gt.sh.booleanactuator.cmd.status"
    )
    Version: Literal["100"] = "100"
