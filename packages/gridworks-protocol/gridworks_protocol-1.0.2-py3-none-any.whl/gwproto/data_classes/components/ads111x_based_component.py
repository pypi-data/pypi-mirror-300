"""Ads111xBasedComponent definition"""

from gwproto.data_classes.components.component import Component
from gwproto.types import Ads111xBasedCacGt, Ads111xBasedComponentGt


class Ads111xBasedComponent(Component[Ads111xBasedComponentGt, Ads111xBasedCacGt]): ...
