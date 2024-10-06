from enum import Enum
from typing import Literal

import canopen.network
from pydantic import Field
from .generic import GenericCanopenNode


class KvaeserCanopenNode(GenericCanopenNode):
    class Config(GenericCanopenNode.Config):
        class Channels(Enum):
            CHANNEL_0 = 0
            CHANNEL_1 = 1
            CHANNEL_2 = 2
            CHANNEL_3 = 3
            CHANNEL_4 = 4
            CHANNEL_5 = 5
            CHANNEL_6 = 6
            CHANNEL_7 = 7

        type: Literal["kvaeser_canopen"]
        channel: Channels = Field(default=Channels.CHANNEL_0, title="Channel to connect to")

        @classmethod
        def default(cls):
            return cls(type="kvaeser_canopen", channel=cls.Channels.CHANNEL_0)

    config: Config

    def __init__(self, config: Config):
        super().__init__(config)

    def init(self):
        self.interface = canopen.network.Network()
        self.interface.connect(
            bustype="kvaser",
            channel=self.config.channel.value,
            bitrate=self.config.bitrate.value,
        )
