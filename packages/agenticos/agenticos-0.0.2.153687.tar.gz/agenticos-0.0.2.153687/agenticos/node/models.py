from enum import Enum
from typing import Callable, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

MSG_HS_NODE = "MSG_HS_NODE"
MSG_HS_ACK = "MSG_HS_ACK"
MSG_TASK_REQ = "MSG_TASK_REQ"
MSG_TASK_FIN = "MSG_TASK_FIN"
MSG_HEARTBEAT = "MSG_HEARTBEAT"


class TaskStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Workflow(BaseModel):
    name: str
    description: str
    inputs: Dict[str, str]
    kickoff_function: Callable[[Dict[str, str]], None] = Field(exclude=True)
    output_function: Callable[[], str] = Field(exclude=True)


class AgenticConfig(BaseModel):
    name: str
    workflows: Dict[str, Workflow] = {}


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    inputs: Dict[str, str]
    status: TaskStatus = Field()
    output: str


class WrongFolderError(Exception):
    pass


class AgenticMessage(BaseModel):
    type: str


class AgenticHandshakeMessage(AgenticMessage):
    type: str = MSG_HS_NODE
    node: str


class TaskFinishedMessage(AgenticMessage):
    type: str = MSG_TASK_FIN
    task_id: str
    status: TaskStatus
    result: str

class TaskRequest(BaseModel):
    workflow: str
    inputs: Dict[str, str]
    task_id: UUID = Field(default_factory=uuid4)
    node_id: str

class AgenticTaskRequestMessage(BaseModel):
    type: str = MSG_TASK_REQ
    task: TaskRequest
