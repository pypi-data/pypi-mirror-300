"""Type ads.channel.config, version 000"""

from typing import Literal, Optional

from pydantic import ConfigDict, PositiveInt

from gwproto.enums import MakeModel, ThermistorDataMethod
from gwproto.property_format import (
    SpaceheatName,
)
from gwproto.types.channel_config import ChannelConfig


class AdsChannelConfig(ChannelConfig):
    ChannelName: SpaceheatName
    TerminalBlockIdx: PositiveInt
    ThermistorMakeModel: MakeModel
    DataProcessingMethod: Optional[ThermistorDataMethod] = None
    DataProcessingDescription: Optional[str] = None
    TypeName: Literal["ads.channel.config"] = "ads.channel.config"
    Version: Literal["000"] = "000"

    model_config = ConfigDict(extra="allow", use_enum_values=True)
