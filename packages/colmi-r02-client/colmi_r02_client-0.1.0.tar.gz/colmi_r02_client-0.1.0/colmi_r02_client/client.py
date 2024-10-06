import asyncio
from collections.abc import Callable
from datetime import datetime, timezone
import logging
from pathlib import Path
from types import TracebackType
from typing import Any

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from colmi_r02_client import (
    battery,
    real_time_hr,
    steps,
    set_time,
    blink_twice,
    hr,
    hr_settings,
)

UART_SERVICE_UUID = "6E40FFF0-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

DEVICE_INFO_UUID = "0000180A-0000-1000-8000-00805F9B34FB"
DEVICE_HW_UUID = "00002A27-0000-1000-8000-00805F9B34FB"
DEVICE_FW_UUID = "00002A26-0000-1000-8000-00805F9B34FB"

logger = logging.getLogger(__name__)


def empty_parse(_packet: bytearray) -> None:
    """Used for commands that we expect a response, but there's nothing in the response"""
    return None


def log_packet(packet: bytearray) -> None:
    print("received: ", packet)


COMMAND_HANDLERS: dict[int, Callable[[bytearray], Any]] = {
    battery.CMD_BATTERY: battery.parse_battery,
    real_time_hr.CMD_START_HEART_RATE: real_time_hr.parse_heart_rate,
    real_time_hr.CMD_STOP_HEART_RATE: empty_parse,
    steps.CMD_GET_STEP_SOMEDAY: steps.SportDetailParser().parse,
    hr.CMD_READ_HEART_RATE: hr.HeartRateLogParser().parse,
    set_time.CMD_SET_TIME: empty_parse,
    hr_settings.CMD_HEART_RATE_LOG_SETTINGS: hr_settings.parse_heart_rate_log_settings,
}
"""
TODO put these somewhere nice

These are commands that we expect to have a response returned for
they must accept a packet as bytearray and then return a value to be put
in the queue for that command type
NOTE: if the value returned is None, it is not added to the queue, this is to support
multi packet messages where the parser has state
"""


class Client:
    def __init__(self, address: str, record_to: Path | None = None):
        self.address = address
        self.bleak_client = BleakClient(self.address)
        self.queues: dict[int, asyncio.Queue] = {cmd: asyncio.Queue() for cmd in COMMAND_HANDLERS}
        self.record_to = record_to

    async def __aenter__(self) -> "Client":
        logger.info(f"Connecting to {self.address}")
        await self.connect()
        logger.info("Connected!")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.disconnect()

    async def connect(self):
        await self.bleak_client.connect()

        nrf_uart_service = self.bleak_client.services.get_service(UART_SERVICE_UUID)
        assert nrf_uart_service
        rx_char = nrf_uart_service.get_characteristic(UART_RX_CHAR_UUID)
        assert rx_char
        self.rx_char = rx_char

        await self.bleak_client.start_notify(UART_TX_CHAR_UUID, self._handle_tx)

    async def disconnect(self):
        await self.bleak_client.disconnect()

    def _handle_tx(self, _: BleakGATTCharacteristic, packet: bytearray) -> None:
        """Bleak callback that handles new packets from the ring."""

        logger.info(f"Received packet {packet}")

        assert len(packet) == 16, f"Packet is the wrong length {packet}"
        packet_type = packet[0]
        assert packet_type < 127, f"Packet has error bit set {packet}"

        if packet_type in COMMAND_HANDLERS:
            result = COMMAND_HANDLERS[packet_type](packet)
            if result is not None:
                self.queues[packet_type].put_nowait(result)
            else:
                logger.debug(f"No result returned from parser for {packet_type}")
        else:
            logger.warning(f"Did not expect this packet: {packet}")

        if self.record_to is not None:
            with self.record_to.open("ab") as f:
                f.write(packet)
                f.write(b"\n")

    async def send_packet(self, packet: bytearray) -> None:
        logger.debug(f"Sending packet: {packet}")
        await self.bleak_client.write_gatt_char(self.rx_char, packet, response=False)

    async def get_battery(self) -> battery.BatteryInfo:
        await self.send_packet(battery.BATTERY_PACKET)
        result = await self.queues[battery.CMD_BATTERY].get()
        assert isinstance(result, battery.BatteryInfo)
        return result

    async def get_realtime_heart_rate(self) -> list[int] | None:
        return await self._poll_real_time_reading(real_time_hr.START_HEART_RATE_PACKET)

    async def _poll_real_time_reading(self, start_packet: bytearray) -> list[int] | None:
        await self.send_packet(start_packet)

        valid_readings: list[int] = []
        error = False
        tries = 0
        while len(valid_readings) < 6 and tries < 20:
            try:
                data: real_time_hr.Reading | real_time_hr.ReadingError = await asyncio.wait_for(
                    self.queues[real_time_hr.CMD_START_HEART_RATE].get(),
                    timeout=2,
                )
                if isinstance(data, real_time_hr.ReadingError):
                    error = True
                    break
                if data.value != 0:
                    valid_readings.append(data.value)
            except TimeoutError:
                tries += 1
                await self.send_packet(real_time_hr.CONTINUE_HEART_RATE_PACKET)

        await self.send_packet(
            real_time_hr.STOP_HEART_RATE_PACKET,
        )
        if error:
            return None
        return valid_readings

    async def get_realtime_spo2(self) -> list[int] | None:
        return await self._poll_real_time_reading(real_time_hr.START_SPO2_PACKET)

    async def set_time(self, ts: datetime) -> None:
        await self.send_packet(set_time.set_time_packet(ts))

    async def blink_twice(self) -> None:
        await self.send_packet(blink_twice.BLINK_TWICE_PACKET)

    async def get_device_info(self) -> dict[str, str]:
        client = self.bleak_client
        data = {}
        device_info_service = client.services.get_service(DEVICE_INFO_UUID)
        assert device_info_service

        hw_info_char = device_info_service.get_characteristic(DEVICE_HW_UUID)
        assert hw_info_char
        hw_version = await client.read_gatt_char(hw_info_char)
        data["hw_version"] = hw_version.decode("utf-8")

        fw_info_char = device_info_service.get_characteristic(DEVICE_FW_UUID)
        assert fw_info_char
        fw_version = await client.read_gatt_char(fw_info_char)
        data["fw_version"] = fw_version.decode("utf-8")

        return data

    async def get_heart_rate_log(self, target: datetime | None = None) -> hr.HeartRateLog | hr.NoData:
        if target is None:
            target = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
        await self.send_packet(hr.read_heart_rate_packet(target))
        return await asyncio.wait_for(
            self.queues[hr.CMD_READ_HEART_RATE].get(),
            timeout=2,
        )

    async def get_heart_rate_log_settings(self) -> hr_settings.HeartRateLogSettings:
        await self.send_packet(hr_settings.READ_HEART_RATE_LOG_SETTINGS_PACKET)
        return await asyncio.wait_for(
            self.queues[hr_settings.CMD_HEART_RATE_LOG_SETTINGS].get(),
            timeout=2,
        )

    async def set_heart_rate_log_settings(self, enabled: bool, interval: int) -> None:
        await self.send_packet(hr_settings.hr_log_settings_packet(hr_settings.HeartRateLogSettings(enabled, interval)))

        # clear response from queue as it's unused and wrong
        await asyncio.wait_for(
            self.queues[hr_settings.CMD_HEART_RATE_LOG_SETTINGS].get(),
            timeout=2,
        )
