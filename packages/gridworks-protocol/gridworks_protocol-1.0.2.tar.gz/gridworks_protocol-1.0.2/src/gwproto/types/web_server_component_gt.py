from typing import Literal

from gwproto.types.component_gt import ComponentGt
from gwproto.types.web_server_gt import WebServerGt


class WebServerComponentGt(ComponentGt):
    WebServer: WebServerGt
    TypeName: Literal["web.server.component.gt"] = "web.server.component.gt"
