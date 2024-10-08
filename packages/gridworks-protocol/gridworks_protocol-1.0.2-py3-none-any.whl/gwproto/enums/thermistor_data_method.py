from enum import auto
from typing import Optional

from gw.enums import GwStrEnum


class ThermistorDataMethod(GwStrEnum):
    """
    What method is used to go from raw voltage readings to captured temperature readings.

    Enum thermistor.data.method version 000 in the GridWorks Type registry.

    Used by multiple Application Shared Languages (ASLs). For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#thermistordatamethod)

    Values:
      - SimpleBeta: Using the beta formula with a calibrated open voltage reading, transmitting
        raw polled data.
      - BetaWithExponentialAveraging: Using the beta formula with a calibrated open voltage
        reading, and then some sort of exponential weighted averaging on polled data.
    """

    SimpleBeta = auto()
    BetaWithExponentialAveraging = auto()

    @classmethod
    def default(cls) -> "ThermistorDataMethod":
        """
        Returns default value (in this case SimpleBeta)
        """
        return cls.SimpleBeta

    @classmethod
    def version(cls, value: Optional[str] = None) -> str:
        if value is None:
            return "000"
        if not isinstance(value, str):
            raise TypeError("This method applies to strings, not enums")
        if value not in value_to_version:
            raise ValueError(f"Unknown enum value: {value}")
        return value_to_version[value]

    @classmethod
    def enum_name(cls) -> str:
        """
        The name in the GridWorks Type Registry (thermistor.data.method)
        """
        return "thermistor.data.method"

    @classmethod
    def enum_version(cls) -> str:
        """
        The version in the GridWorks Type Registry (000)
        """
        return "000"


value_to_version = {
    "SimpleBeta": "000",
    "BetaWithExponentialAveraging": "000",
}
