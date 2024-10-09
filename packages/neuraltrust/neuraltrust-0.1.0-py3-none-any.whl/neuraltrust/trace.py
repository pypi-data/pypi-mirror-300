import uuid
import typing
import datetime as dt
from .api_client import (
    User,
    Metadata
)

class Trace:
    def __init__(self, client, conversation_id: str = None, channel_id: str = None, session_id: str = None, user: typing.Optional[User] = None, metadata: typing.Optional[Metadata] = None, custom: typing.Optional[dict] = None):
        self.client = client
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.session_id = session_id
        self.interaction_id = str(uuid.uuid4())
        self.channel_id = channel_id
        self.user = user
        self.metadata = metadata
        self.custom = custom
        self.start_timestamp = None
        self.end_timestamp = None
        self.input = None
        self.output = None
        self.task = None

    def retrieval(self, input: str):
        self.input = input
        self.task = "retrieval"
        self.start_timestamp = int(dt.datetime.now().timestamp())
        return self

    def generation(self, input: str):
        self.input = input
        self.task = "generation"
        self.start_timestamp = int(dt.datetime.now().timestamp())
        return self

    def router(self, input: str):
        self.input = input
        self.task = "router"
        self.start_timestamp = int(dt.datetime.now().timestamp())
        return self

    def event(self, input: str):
        self.input = input
        self.task = "event"
        self.start_timestamp = int(dt.datetime.now().timestamp())
        self._send_trace()

    def system(self, input: str|object):
        self.input = str(input)
        self.task = "system"
        self.start_timestamp = int(dt.datetime.now().timestamp())
        self.end_timestamp = int(dt.datetime.now().timestamp())
        self._send_trace()

    def end(self, output: str|object):
        self.output = str(output)
        self.end_timestamp = int(dt.datetime.now().timestamp())
        self._send_trace()
    
    def _send_trace(self):
        self.client._trace(
            type="traces",
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            interaction_id=self.interaction_id,
            user=self.user,
            metadata=self.metadata,
            input=self.input,
            output=self.output,
            task=self.task,
            custom=str(self.custom),
            start_timestamp=self.start_timestamp * 1000,
            end_timestamp=self.end_timestamp * 1000
        )
        self.input = None
        self.output = None
        self.task = None
        self.start_timestamp = None
        self.end_timestamp = None