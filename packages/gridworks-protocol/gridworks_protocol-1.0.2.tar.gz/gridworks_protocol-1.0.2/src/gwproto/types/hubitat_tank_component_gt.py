from typing import Literal

from gwproto.types.component_gt import ComponentGt
from gwproto.types.hubitat_tank_gt import HubitatTankSettingsGt


class HubitatTankComponentGt(ComponentGt):
    Tank: HubitatTankSettingsGt
    TypeName: Literal["hubitat.tank.component.gt"] = "hubitat.tank.component.gt"
