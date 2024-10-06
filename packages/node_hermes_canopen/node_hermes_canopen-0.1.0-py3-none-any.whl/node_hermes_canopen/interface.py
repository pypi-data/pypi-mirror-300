from qtpy import QtWidgets

from .universal_node import CanopenNode
from .ui.interface import Ui_Form
from node_hermes_qt.nodes.generic_qt_node import GenericNodeWidget
from node_hermes_canopen.nodes import KvaeserCanopenNode, Usb2CanCanopenNode, LinuxCanopenNode


def interface_to_index(interface: CanopenNode.Config.SelectedInterface) -> int:
    if interface == CanopenNode.Config.SelectedInterface.KVAESER:
        return 0
    elif interface == CanopenNode.Config.SelectedInterface.USB2CAN:
        return 1
    elif interface == CanopenNode.Config.SelectedInterface.LINUX:
        return 2
    else:
        raise ValueError("Invalid interface selected")


def index_to_interface(index: int) -> CanopenNode.Config.SelectedInterface:
    if index == 0:
        return CanopenNode.Config.SelectedInterface.KVAESER
    elif index == 1:
        return CanopenNode.Config.SelectedInterface.USB2CAN
    elif index == 2:
        return CanopenNode.Config.SelectedInterface.LINUX
    else:
        raise ValueError("Invalid index selected")


class CanopenConfigurationWidget(GenericNodeWidget, Ui_Form):
    kvaeser_channel: QtWidgets.QComboBox
    kvaeser_bitrate: QtWidgets.QComboBox
    allow_update: bool = True

    def __init__(self, node: "CanopenNode"):
        super().__init__(node)
        self.setupUi(self)
        self.node = node

        # Set allowed values for the channel
        self.kvaeser_channel.clear()
        self.kvaeser_channel.addItems([str(channel.value) for channel in KvaeserCanopenNode.Config.Channels])
        self.kvaeser_bitrate.clear()
        self.kvaeser_bitrate.addItems([str(bitrate.value) for bitrate in KvaeserCanopenNode.Config.Bitrates])
        self.can2usb_bitrate.clear()
        self.can2usb_bitrate.addItems([str(bitrate.value) for bitrate in Usb2CanCanopenNode.Config.Bitrates])
        self.linuxcan_bitrate.clear()
        self.linuxcan_bitrate.addItems([str(bitrate.value) for bitrate in LinuxCanopenNode.Config.Bitrates])

        # # select connection widget
        # self.connect_widget = QConnectionDisplayWidget(self.component)
        # self.connect_widget.state_update_signal.connect(self.update_ui)
        # self.connectLayout.addWidget(self.connect_widget)

        # Connect signals
        # self.kvaeser_channel.currentIndexChanged.connect(self.save_config)
        # self.kvaeser_bitrate.currentIndexChanged.connect(self.save_config)

        # self.can2usb_bitrate.currentIndexChanged.connect(self.save_config)
        # self.can2usb_serial.textChanged.connect(self.save_config)

        # self.linuxcan_bitrate.currentIndexChanged.connect(self.save_config)
        # self.linuxcan_interface.textChanged.connect(self.save_config)

        # self.enable_sync.stateChanged.connect(self.save_config)
        # self.sync_frequency.valueChanged.connect(self.save_config)
        # self.tabWidget.currentChanged.connect(self.save_config)

        self.on_change_widgets = [
            self.kvaeser_channel,
            self.kvaeser_bitrate,
            self.can2usb_bitrate,
            self.can2usb_serial,
            self.linuxcan_bitrate,
            self.linuxcan_interface,
            self.enable_sync,
            self.sync_frequency,
            self.tabWidget,
        ]
        for widget in self.on_change_widgets:
            if isinstance(widget, QtWidgets.QComboBox):
                widget.currentIndexChanged.connect(self.save_config)
            elif isinstance(widget, QtWidgets.QLineEdit):
                widget.textChanged.connect(self.save_config)
            elif isinstance(widget, QtWidgets.QCheckBox):
                widget.stateChanged.connect(self.save_config)
            elif isinstance(widget, QtWidgets.QSpinBox):
                widget.valueChanged.connect(self.save_config)
            elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                widget.valueChanged.connect(self.save_config)
            elif isinstance(widget, QtWidgets.QTabWidget):
                widget.currentChanged.connect(self.save_config)
            else:
                raise NotImplementedError(f"Widget {widget} not implemented")

        self.from_config(node.config)

        self.setStyleSheet(
            """:disabled{
            background-color: lightgray;
            color: gray;
            }"""
        )

    def set_enabled(self, enabled: bool):
        self.kvaeser_channel.setEnabled(enabled)
        self.kvaeser_bitrate.setEnabled(enabled)
        self.enable_sync.setEnabled(enabled)
        self.sync_frequency.setEnabled(enabled)
        self.tabWidget.setEnabled(enabled)

    def from_config(self, config: CanopenNode.Config):
        self.allow_update = False

        self.kvaeser_channel.setCurrentText(str(config.kvaeser_config.channel.value))
        self.kvaeser_bitrate.setCurrentText(str(config.kvaeser_config.bitrate.value))

        self.can2usb_bitrate.setCurrentText(str(config.usb2can_config.bitrate.value))
        self.can2usb_serial.setText(config.usb2can_config.serial)

        self.linuxcan_bitrate.setCurrentText(str(config.linux_config.bitrate.value))
        self.linuxcan_interface.setText(config.linux_config.channel)

        self.enable_sync.setChecked(config.enable_sync)
        self.sync_frequency.setValue(config.sync_frequency)
        self.tabWidget.setCurrentIndex(interface_to_index(config.selected_interface))
        self.allow_update = True

    def update_config(self, config: CanopenNode.Config):
        if not self.allow_update:
            return

        self.node.config.kvaeser_config.channel = KvaeserCanopenNode.Config.Channels(
            int(self.kvaeser_channel.currentText())
        )
        self.node.config.kvaeser_config.bitrate = KvaeserCanopenNode.Config.Bitrates(
            int(self.kvaeser_bitrate.currentText())
        )

        self.node.config.usb2can_config.serial = self.can2usb_serial.text()

        self.node.config.usb2can_config.bitrate = Usb2CanCanopenNode.Config.Bitrates(
            int(self.kvaeser_bitrate.currentText())
        )

        self.node.config.linux_config.bitrate = LinuxCanopenNode.Config.Bitrates(
            int(self.kvaeser_bitrate.currentText())
        )

        self.node.config.linux_config.channel = self.linuxcan_interface.text()
        self.node.config.selected_interface = index_to_interface(self.tabWidget.currentIndex())
        self.node.config.enable_sync = self.enable_sync.isChecked()
        self.node.config.sync_frequency = self.sync_frequency.value()

    def save_config(self):
        self.update_config(self.node.config)
        print(self.node.config)

    # def load_config(self):
    #     assert self.node.config.kvaeser_config is not None, "Kvaeser interface configuration is required"
    #     self.kvaeser_channel.setCurrentText(str(self.node.config.kvaeser_config.channel.value))
    #     self.kvaeser_bitrate.setCurrentText(str(self.node.config.kvaeser_config.bitrate.value))
    #     self.enable_sync.setChecked(self.node.config.enable_sync)
    #     self.sync_frequency.setValue(self.node.config.sync_frequency)
    #     if self.node.config.interface == CanopenNode.Config.Interface.KVAESER:
    #         self.tabWidget.setCurrentIndex(0)
    #     else:
    #         self.tabWidget.setCurrentIndex(1)

    # def save_config(self):
    #     assert self.node.config.kvaeser_config is not None, "Kvaeser interface configuration is required"
    #     self.node.config.kvaeser_config.channel = KvaeserCanopenInterfaceComponent.Config.Channels(
    #         int(self.kvaeser_channel.currentText())
    #     )
    #     self.node.config.kvaeser_config.bitrate = KvaeserCanopenInterfaceComponent.Config.Bitrates(
    #         int(self.kvaeser_bitrate.currentText())
    #     )
    #     self.node.config.enable_sync = self.enable_sync.isChecked()
    #     self.node.config.sync_frequency = self.sync_frequency.value()
    #     if self.tabWidget.currentIndex() == 0:
    #         self.node.config.interface = CanopenNode.Config.Interface.KVAESER
    #     else:
    #         self.node.config.interface = CanopenNode.Config.Interface.SOCKETCAN

    def update_ui(self):
        # If connected, disable the address line edit and selection widget
        is_connected = self.node.state not in [
            self.node.State.STOPPED,
            self.node.State.ERROR,
            self.node.State.IDLE,
        ]

        self.kvaeser_channel.setEnabled(not is_connected)
        self.kvaeser_bitrate.setEnabled(not is_connected)
        self.enable_sync.setEnabled(not is_connected)
        self.sync_frequency.setEnabled(not is_connected and self.enable_sync.isChecked())
        self.tabWidget.setEnabled(not is_connected)
