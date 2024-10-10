import json
from threading import Event, Lock, Thread
from uuid import UUID

import websocket

from agenticos.node.models import *
from agenticos.node.settings import settings
from agenticos.node.http_support import HTTPHealthServer

tasks: dict[UUID, Task] = {}


class RepeatTimer(Thread):
    def __init__(self, event, callback):
        Thread.__init__(self)
        self._stopped = event
        self._callback = callback

    def run(self):
        while not self._stopped.wait(10):
            self._callback()


class WSNode:
    def __init__(self, registry: str, config: AgenticConfig):
        self.registry = registry
        self.config = config
        self.lock = Lock()
        self.id = None

    def run_task(self, workflow: Workflow, task: Task) -> None:
        try:
            workflow.kickoff_function(task.inputs)
            task.output = workflow.output_function()
            task.status = TaskStatus.COMPLETED
        except Exception as e:
            task.output = str(e)
            task.status = TaskStatus.FAILED

    def on_message(self, ws, msg):
        message = json.loads(msg)
        if "type" not in message:
            print("Unknown message format", message)
        if message["type"] == MSG_HS_ACK:
            print("Handshake successful")
            self.id = message["id"]
        elif message["type"] == MSG_TASK_REQ:
            print("Task request: ", message)
            t_req = AgenticTaskRequestMessage(**message)
            task = Task(
                id=t_req.task.task_id,
                inputs=t_req.task.inputs,
                status=TaskStatus.RUNNING,
                output="",
            )
            tasks[t_req.task.task_id] = task
            workflow = self.config.workflows[t_req.task.workflow]
            thread = Thread(target=self.run_and_report, args=(workflow, task))
            thread.start()

    def run_and_report(self, workflow: Workflow, task: Task):
        print("Running task", task.id)
        self.run_task(workflow, task)
        tf_msg = TaskFinishedMessage(
            task_id=str(task.id), status=task.status, result=task.output
        )
        print("Sending task finished message", tf_msg.model_dump())
        self.send_ws_message(json.dumps(tf_msg.model_dump()))

    def send_ws_message(self, message):
        # Make sure that only one thread is sending messages at a time
        with self.lock:
            self.ws.send(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        self.stopFlag.set()
        self.health_http_server.stop()
        print("### closed ###")

    def on_open(self, ws):
        if settings.HTTP_HEALTHCHECK:
            self.health_http_server = HTTPHealthServer(settings.HTTP_PORT)
            self.health_http_server.start()
        payload = json.dumps(self.config.model_dump())
        ws.send(payload)
        self._init_heartbeat()

    def send_heartbeat(self):
        print("Sending heartbeat")
        self.send_ws_message(self.hearbeat_msg)

    def _init_heartbeat(self):
        print("Init heartbeat")
        self.hearbeat_msg = json.dumps(AgenticMessage(type=MSG_HEARTBEAT).model_dump())
        self.stopFlag = Event()
        thread = RepeatTimer(self.stopFlag, self.send_heartbeat)
        thread.start()
        # this will stop the timer

    def connect_to_registry(self) -> None:
        websocket.enableTrace(True)
        hdrs = []
        if settings.AUTH_TOKEN != "":
            hdrs.append("Authorization:Bearer " + settings.AUTH_TOKEN)
        self.ws = websocket.WebSocketApp(
            self.registry + "/ws/nodes/connect",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            header=hdrs,
        )
        self.ws.run_forever()
