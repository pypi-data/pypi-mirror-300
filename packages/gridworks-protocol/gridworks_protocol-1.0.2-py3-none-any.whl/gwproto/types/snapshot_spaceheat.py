"""Type snapshot.spaceheat, version 001"""

from typing import List, Literal

from pydantic import BaseModel, ConfigDict

from gwproto.property_format import (
    LeftRightDotStr,
    UTCMilliseconds,
    UUID4Str,
)
from gwproto.types.single_reading import SingleReading


class SnapshotSpaceheat(BaseModel):
    FromGNodeAlias: LeftRightDotStr
    FromGNodeInstanceId: UUID4Str
    SnapshotTimeUnixMs: UTCMilliseconds
    LatestReadingList: List[SingleReading]
    TypeName: Literal["snapshot.spaceheat"] = "snapshot.spaceheat"
    Version: Literal["001"] = "001"

    model_config = ConfigDict(use_enum_values=True)
