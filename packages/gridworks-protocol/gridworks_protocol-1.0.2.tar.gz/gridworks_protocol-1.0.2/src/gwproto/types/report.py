"""Type report, version 000"""

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, PositiveInt, model_validator
from typing_extensions import Self

from gwproto.property_format import (
    LeftRightDotStr,
    UTCMilliseconds,
    UTCSeconds,
    UUID4Str,
)
from gwproto.types.channel_readings import ChannelReadings


class Report(BaseModel):
    FromGNodeAlias: LeftRightDotStr
    FromGNodeInstanceId: UUID4Str
    AboutGNodeAlias: LeftRightDotStr
    SlotStartUnixS: UTCSeconds
    BatchedTransmissionPeriodS: PositiveInt
    ChannelReadingList: List[ChannelReadings]
    MessageCreatedMs: UTCMilliseconds
    Id: UUID4Str
    TypeName: Literal["report"] = "report"
    Version: Literal["000"] = "000"

    model_config = ConfigDict(extra="allow", use_enum_values=True)

    @model_validator(mode="after")
    def check_axiom_1(self) -> Self:
        """
        Axiom 1: Time Consistency.
        For every ScadaReadTimeUnixMs   let read_s = read_ms / 1000.  Let start_s be SlotStartUnixS.  Then read_s >= start_s and start_s + BatchedTransmissionPeriodS + 1 + start_s > read_s.
        """
        # Implement check for axiom 1"

        return self

    @model_validator(mode="after")
    def check_axiom_2(self) -> Self:
        """
        Axiom 2: Unique Channel names and Ids
        """

        ids = [cr.ChannelId for cr in self.ChannelReadingList]
        if len(ids) != len(set(ids)):
            raise ValueError(
                "Axiom 1 violated! ChannelReadingList ChannelIds must be unique"
            )
        names = [cr.ChannelName for cr in self.ChannelReadingList]
        if len(names) != len(set(names)):
            raise ValueError(
                "Axiom 1 violated! ChannelReadingList ChannelNames must be unique"
            )
        return self
