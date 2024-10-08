from enum import auto
from typing import Optional

from gw.enums import GwStrEnum


class Unit(GwStrEnum):
    """
    Specifies the physical unit of sensed data reported by SCADA

    Enum spaceheat.unit version 001 in the GridWorks Type registry.

    Used by multiple Application Shared Languages (ASLs). For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#spaceheatunit)

    Values:
      - Unknown
      - Unitless
      - W
      - Celcius
      - Fahrenheit
      - Gpm
      - WattHours
      - AmpsRms
      - VoltsRms
      - Gallons
      - ThermostatStateEnum
    """

    Unknown = auto()
    Unitless = auto()
    W = auto()
    Celcius = auto()
    Fahrenheit = auto()
    Gpm = auto()
    WattHours = auto()
    AmpsRms = auto()
    VoltsRms = auto()
    Gallons = auto()
    ThermostatStateEnum = auto()

    @classmethod
    def default(cls) -> "Unit":
        """
        Returns default value (in this case Unknown)
        """
        return cls.Unknown

    @classmethod
    def version(cls, value: Optional[str] = None) -> str:
        if value is None:
            return "001"
        if not isinstance(value, str):
            raise TypeError("This method applies to strings, not enums")
        if value not in value_to_version:
            raise ValueError(f"Unknown enum value: {value}")
        return value_to_version[value]

    @classmethod
    def enum_name(cls) -> str:
        """
        The name in the GridWorks Type Registry (spaceheat.unit)
        """
        return "spaceheat.unit"

    @classmethod
    def enum_version(cls) -> str:
        """
        The version in the GridWorks Type Registry (001)
        """
        return "001"


value_to_version = {
    "Unknown": "000",
    "Unitless": "000",
    "W": "000",
    "Celcius": "000",
    "Fahrenheit": "000",
    "Gpm": "000",
    "WattHours": "000",
    "AmpsRms": "000",
    "VoltsRms": "000",
    "Gallons": "000",
    "ThermostatStateEnum": "001",
}
