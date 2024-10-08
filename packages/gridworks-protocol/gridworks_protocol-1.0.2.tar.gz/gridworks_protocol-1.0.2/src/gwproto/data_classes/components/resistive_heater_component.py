"""ResistiveHeaterComponent definition"""

from gwproto.data_classes.components.component import Component
from gwproto.types import ResistiveHeaterCacGt, ResistiveHeaterComponentGt


class ResistiveHeaterComponent(
    Component[ResistiveHeaterComponentGt, ResistiveHeaterCacGt]
): ...
