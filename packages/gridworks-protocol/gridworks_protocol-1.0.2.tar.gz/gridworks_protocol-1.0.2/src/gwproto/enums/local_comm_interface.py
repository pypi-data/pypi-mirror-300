from enum import auto

from gw.enums import GwStrEnum


class LocalCommInterface(GwStrEnum):
    """
    Categorization of in-house comm mechanisms for SCADA

    Enum local.comm.interface version 000 in the GridWorks Type registry.

    Used by used by multiple Application Shared Languages (ASLs), including but not limited to
    gwproto. For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#localcomminterface)

    Values (with symbols in parens):
      - Unknown (00000000)
      - I2C (9ec8bc49)
      - Ethernet (c1e7a955)
      - OneWire (ae2d4cd8)
      - RS485 (a6a4ac9f)
      - SimRabbit (efc144cd)
      - Wifi (46ac6589)
      - Analog_4_20_mA (653c73b8)
      - RS232 (0843a726)
    """

    UNKNOWN = auto()
    I2C = auto()
    ETHERNET = auto()
    ONEWIRE = auto()
    RS485 = auto()
    SIMRABBIT = auto()
    WIFI = auto()
    ANALOG_4_20_MA = auto()
    RS232 = auto()

    @classmethod
    def default(cls) -> "LocalCommInterface":
        """
        Returns default value (in this case UNKNOWN)
        """
        return cls.UNKNOWN

    @classmethod
    def version(cls, value: str) -> str:
        """
        Returns the version of an enum value.

        Once a value belongs to one version of the enum, it belongs
        to all future versions.

        Args:
            value (str): The candidate enum value.

        Raises:
            ValueError: If value is not one of the enum values.

        Returns:
            str: The earliest version of the enum containing value.
        """
        if not isinstance(value, str):
            raise ValueError("This method applies to strings, not enums")  # noqa: TRY004
        if value not in value_to_version:
            raise ValueError(f"Unknown enum value: {value}")
        return value_to_version[value]

    @classmethod
    def enum_name(cls) -> str:
        """
        The name in the GridWorks Type Registry (local.comm.interface)
        """
        return "local.comm.interface"

    @classmethod
    def enum_version(cls) -> str:
        """
        The version in the GridWorks Type Registry (000)
        """
        return "000"


value_to_version = {
    "UNKNOWN": "000",
    "I2C": "000",
    "ETHERNET": "000",
    "ONEWIRE": "000",
    "RS485": "000",
    "SIMRABBIT": "000",
    "WIFI": "000",
    "ANALOG_4_20_MA": "000",
    "RS232": "000",
}
