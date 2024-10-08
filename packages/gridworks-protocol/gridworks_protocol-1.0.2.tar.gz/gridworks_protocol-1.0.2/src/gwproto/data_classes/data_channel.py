from pydantic import ConfigDict

from gwproto.data_classes.sh_node import ShNode
from gwproto.types import DataChannelGt


class DataChannel(DataChannelGt):
    about_node: ShNode
    captured_by_node: ShNode

    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=True)

    def __hash__(self) -> int:
        return hash(self.Id)
