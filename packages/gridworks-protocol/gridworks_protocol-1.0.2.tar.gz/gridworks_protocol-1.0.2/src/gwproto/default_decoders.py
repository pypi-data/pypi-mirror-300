# ruff: noqa: ANN401, RUF100,


import gwproto.types.cacs
import gwproto.types.components
from gwproto.decoders import CacDecoder, ComponentDecoder

default_cac_decoder = CacDecoder(
    model_name="DefaultCacDecoder",
    modules=[gwproto.types.cacs],
)

default_component_decoder = ComponentDecoder(
    model_name="DefaultComponentDecoder",
    modules=[gwproto.types.components],
)
