"""Type channel.config, version 000"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, PositiveInt, StrictInt, model_validator
from typing_extensions import Self

from gwproto.enums import Unit
from gwproto.property_format import (
    SpaceheatName,
)


class ChannelConfig(BaseModel):
    ChannelName: SpaceheatName
    PollPeriodMs: PositiveInt
    CapturePeriodS: PositiveInt
    AsyncCapture: bool
    AsyncCaptureDelta: Optional[PositiveInt] = None
    Exponent: StrictInt
    Unit: Unit
    TypeName: Literal["channel.config"] = "channel.config"
    Version: Literal["000"] = "000"

    model_config = ConfigDict(use_enum_values=True)

    def __hash__(self) -> int:
        return hash(self.ChannelName)

    @model_validator(mode="after")
    def check_axiom_1(self) -> Self:
        """
        Axiom 1: Async Capture Consistency.
        If AsyncCapture is True, then AsyncCaptureDelta exists
        """
        if self.AsyncCapture and not self.AsyncCaptureDelta:
            raise ValueError(
                "Axiom 1 violated! If AsyncCapture is true, "
                "then AsyncCaptureDelta must exist"
            )
        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> Self:
        """
        Axiom 2: Capture and Polling Consistency.
        CapturePeriodMs (CapturePeriodS * 1000) must be larger than PollPeriodMs. If CapturePeriodMs < 10 * PollPeriodMs then CapturePeriodMs must be a multiple of PollPeriodMs.
        """
        # Implement check for axiom 2"
        return self
