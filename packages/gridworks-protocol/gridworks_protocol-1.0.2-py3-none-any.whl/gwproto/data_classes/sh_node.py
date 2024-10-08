"""ShNode definition"""

from typing import Optional

from pydantic import ConfigDict

from gwproto.data_classes.components.component import Component
from gwproto.enums import ActorClass
from gwproto.types import SpaceheatNodeGt


class ShNode(SpaceheatNodeGt):
    """
    A SpaceheatNode, or ShNode, is an organizing principal for the SCADA software.
    ShNodes can represent both underlying physical objects (water tank), measurements of these
    objects (temperature sensing at the top of a water tank), and actors within the code
    (an actor measuring multiple temperatures, or an actor responsible for filtering/smoothing
    temperature data for the purposes of thermostatic control).
    """

    component: Optional[Component] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __hash__(self) -> int:
        return hash(self.ShNodeId)

    @property
    def sh_node_id(self) -> str:
        return self.ShNodeId

    @property
    def name(self) -> str:
        return self.Name

    @property
    def actor_class(self) -> ActorClass:
        return self.ActorClass

    @property
    def display_name(self) -> Optional[str]:
        return self.DisplayName

    @property
    def component_id(self) -> Optional[str]:
        return self.ComponentId

    @property
    def in_power_metering(self) -> Optional[bool]:
        return self.InPowerMetering

    def __repr__(self) -> str:
        rs = f"ShNode {self.display_name} => {self.name}, "
        if self.has_actor:
            rs += f" ({self.actor_class})"
        else:
            rs += " (passive, no actor)"
        return rs

    @property
    def has_actor(self) -> bool:
        return self.actor_class != ActorClass.NoActor
