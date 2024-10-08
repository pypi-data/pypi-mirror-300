from enum import auto
from typing import Optional

from gw.enums import GwStrEnum


class TelemetryName(GwStrEnum):
    """
    Specifies the name of sensed data reported by a Spaceheat SCADA

    Enum spaceheat.telemetry.name version 001 in the GridWorks Type registry.

    Used by multiple Application Shared Languages (ASLs). For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#spaceheattelemetryname)
      - [More Info](https://gridworks-protocol.readthedocs.io/en/latest/telemetry-name.html)

    Values:
      - Unknown: Default Value - unknown telemetry name.
      - PowerW: Power in Watts.
      - RelayState: The Telemetry reading belongs to ['Energized', 'DeEnergized'] (relay.energization.state
        enum).
      - WaterTempCTimes1000: Water temperature, in Degrees Celcius multiplied by 1000.
        Example: 43200 means 43.2 deg Celcius.
      - WaterTempFTimes1000: Water temperature, in Degrees F multiplied by 1000. Example:
        142100 means 142.1 deg Fahrenheit.
      - GpmTimes100: Gallons Per Minute multiplied by 100. Example: 433 means 4.33 gallons
        per minute.
      - CurrentRmsMicroAmps: Current measurement in Root Mean Square MicroAmps.
      - GallonsTimes100: Gallons multipled by 100. This is useful for flow meters that
        report cumulative gallons as their raw output. Example: 55300 means 55.3 gallons.
      - VoltageRmsMilliVolts: Voltage in Root Mean Square MilliVolts.
      - MilliWattHours: Energy in MilliWattHours.
      - FrequencyMicroHz: Frequency in MicroHz. Example: 59,965,332 means 59.965332 Hz.
      - AirTempCTimes1000: Air temperature, in Degrees Celsius multiplied by 1000. Example:
        6234 means 6.234 deg Celcius.
      - AirTempFTimes1000: Air temperature, in Degrees F multiplied by 1000. Example:
        69329 means 69.329 deg Fahrenheit.
      - ThermostatState: Thermostat State: 0 means idle, 1 means heating, 2 means pending
        heat
    """

    Unknown = auto()
    PowerW = auto()
    RelayState = auto()
    WaterTempCTimes1000 = auto()
    WaterTempFTimes1000 = auto()
    GpmTimes100 = auto()
    CurrentRmsMicroAmps = auto()
    GallonsTimes100 = auto()
    VoltageRmsMilliVolts = auto()
    MilliWattHours = auto()
    FrequencyMicroHz = auto()
    AirTempCTimes1000 = auto()
    AirTempFTimes1000 = auto()
    ThermostatState = auto()

    @classmethod
    def default(cls) -> "TelemetryName":
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
        The name in the GridWorks Type Registry (spaceheat.telemetry.name)
        """
        return "spaceheat.telemetry.name"

    @classmethod
    def enum_version(cls) -> str:
        """
        The version in the GridWorks Type Registry (001)
        """
        return "001"


value_to_version = {
    "Unknown": "000",
    "PowerW": "000",
    "RelayState": "000",
    "WaterTempCTimes1000": "000",
    "WaterTempFTimes1000": "000",
    "GpmTimes100": "000",
    "CurrentRmsMicroAmps": "000",
    "GallonsTimes100": "000",
    "VoltageRmsMilliVolts": "001",
    "MilliWattHours": "001",
    "FrequencyMicroHz": "001",
    "AirTempCTimes1000": "001",
    "AirTempFTimes1000": "001",
    "ThermostatState": "001",
}
