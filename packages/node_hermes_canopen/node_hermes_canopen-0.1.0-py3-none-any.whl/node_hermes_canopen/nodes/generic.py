import canopen.network
from node_hermes_core.nodes import GenericNode

from pydantic import Field
from enum import Enum


class GenericCanopenNode(GenericNode):
    interface: canopen.network.Network | None = None

    class Config(GenericNode.Config):
        class Bitrates(Enum):
            BITRATE_1000000 = 1000000
            BITRATE_500000 = 500000
            BITRATE_250000 = 250000
            BITRATE_125000 = 125000

        bitrate: Bitrates = Field(default=Bitrates.BITRATE_1000000, title="Bitrate")

    def deinit(self):
        assert self.interface is not None, "Interface is not initialized"
        self.interface.disconnect()
        super().deinit()
