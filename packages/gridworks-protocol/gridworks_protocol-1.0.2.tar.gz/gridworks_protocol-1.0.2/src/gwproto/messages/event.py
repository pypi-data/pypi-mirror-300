import time
import uuid
from enum import Enum
from typing import Any, Generic, Literal, Optional, TypeVar

from pydantic import BaseModel, Field, field_validator

from gwproto.message import Message, as_enum
from gwproto.types import Report, SnapshotSpaceheat


class EventBase(BaseModel):
    MessageId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    TimeNS: int = Field(default_factory=time.time_ns)
    Src: str = ""
    TypeName: str


class AnyEvent(EventBase, extra="allow"):
    MessageId: str
    TimeNS: int
    Src: str
    TypeName: str


EventT = TypeVar("EventT", bound=EventBase)


class EventMessage(Message[EventT], Generic[EventT]):
    def __init__(self, AckRequired: bool = True, **kwargs: Any) -> None:  # noqa: ANN401, FBT001, FBT002, N803
        super().__init__(AckRequired=AckRequired, **kwargs)


class StartupEvent(EventBase):
    TypeName: Literal["gridworks.event.startup"] = "gridworks.event.startup"


class ShutdownEvent(EventBase):
    Reason: str
    TypeName: Literal["gridworks.event.shutdown"] = "gridworks.event.shutdown"


class Problems(Enum):
    error = "error"
    warning = "warning"


class ProblemEvent(EventBase):
    ProblemType: Problems
    Summary: str
    Details: str = ""
    TypeName: Literal["gridworks.event.problem"] = "gridworks.event.problem"

    @field_validator("ProblemType", mode="before")
    @classmethod
    def problem_type_value(cls, v: Any) -> Optional[Problems]:  # noqa: ANN401
        return as_enum(v, Problems, Problems.error)


class CommEvent(EventBase):
    PeerName: str


class MQTTCommEvent(CommEvent): ...


class MQTTConnectEvent(MQTTCommEvent):
    TypeName: Literal["gridworks.event.comm.mqtt.connect"] = (
        "gridworks.event.comm.mqtt.connect"
    )


class MQTTConnectFailedEvent(MQTTCommEvent):
    TypeName: Literal["gridworks.event.comm.mqtt.connect.failed"] = (
        "gridworks.event.comm.mqtt.connect.failed"
    )


class MQTTDisconnectEvent(MQTTCommEvent):
    TypeName: Literal["gridworks.event.comm.mqtt.disconnect"] = (
        "gridworks.event.comm.mqtt.disconnect"
    )


class MQTTFullySubscribedEvent(CommEvent):
    TypeName: Literal["gridworks.event.comm.mqtt.fully.subscribed"] = (
        "gridworks.event.comm.mqtt.fully.subscribed"
    )


class ResponseTimeoutEvent(CommEvent):
    TypeName: Literal["gridworks.event.comm.response.timeout"] = (
        "gridworks.event.comm.response.timeout"
    )


class PeerActiveEvent(CommEvent):
    TypeName: Literal["gridworks.event.comm.peer.active"] = (
        "gridworks.event.comm.peer.active"
    )


class ReportEvent(EventBase):
    Report: Report
    TypeName: Literal["gridworks.event.report"] = "gridworks.event.report"


class SnapshotSpaceheatEvent(EventBase):
    Snap: SnapshotSpaceheat
    TypeName: Literal["gridworks.event.snapshot.spaceheat"] = (
        "gridworks.event.snapshot.spaceheat"
    )
