from typing import Dict, Literal

from node_hermes_core.depencency.node_dependency import NodeDependency
from node_hermes_core.nodes import GenericNode
from pydantic import BaseModel, Field, PrivateAttr

from ..network import GenericCanopenNetworkNode, KvaeserCanopenNetworkNode
from .device import CanopenDevice
from .mock_device import CanopenMockDevice


class PDOConfigModel(BaseModel):
    format: str
    _name: str = PrivateAttr()
    pdo_id: int


class CanopenDeviceNode(GenericNode):
    class Config(GenericNode.Config):
        type: Literal["canopen_device"]
        device_id: int = Field(description="The device ID for the node")

        eds_path: str = Field(title="EDS Path", description="Path to the EDS file for the node")

        mock: bool = False
        canopen_interface: GenericCanopenNetworkNode.Config | str | None = Field(
            description="The canopen interface to use for the node, either a string or a config object"
        )

    config: Config
    canopen_interface: GenericCanopenNetworkNode | None = None
    device: CanopenDevice | CanopenMockDevice | None = None

    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.base_dependency = NodeDependency(
            name="interface", config=config.canopen_interface, reference=KvaeserCanopenNetworkNode
        )
        self.dependency_manager.add(self.base_dependency)

    def init(self, canopen_interface: GenericCanopenNetworkNode) -> None:  # type: ignore
        self.canopen_interface = canopen_interface

        assert (
            self.canopen_interface.interface is not None
        ), "Canopen interface must be initialized before initializing the device"

        # Initialize the device interface
        if not self.config.mock:
            self.device = CanopenDevice(self.canopen_interface, self.config.eds_path, self.config.device_id)
        else:
            self.device = CanopenMockDevice(self.canopen_interface, self.config.eds_path, self.config.device_id)


    def deinit(self):
        if self.device is not None:
            self.device.close()
            self.device = None
        return super().deinit()

    def watch_state(self):
        assert self.device is not None, "Device interface must be initialized before watching state"
        self.device.connection_manager.update()


# This should be present in the base canopen interface
# Check if sync has stopped, and restart it if it has
# if self.enable_sync and self.network.sync._task._task.stopped:  # type: ignore
#     self.network.sync.start(1 / self.sync_rate)

# self.network.check()
