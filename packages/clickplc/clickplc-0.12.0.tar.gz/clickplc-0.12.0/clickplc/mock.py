"""
Python mock driver for AutomationDirect (formerly Koyo) ClickPLCs.

Uses local storage instead of remote communications.

Distributed under the GNU General Public License v2
Copyright (C) 2021 NuMat Technologies
"""
from collections import defaultdict
from unittest.mock import MagicMock

try:  # pymodbus >= 3.7.0
    from pymodbus.pdu.bit_read_message import ReadCoilsResponse, ReadDiscreteInputsResponse
    from pymodbus.pdu.bit_write_message import WriteMultipleCoilsResponse, WriteSingleCoilResponse
    from pymodbus.pdu.register_read_message import ReadHoldingRegistersResponse
    from pymodbus.pdu.register_write_message import WriteMultipleRegistersResponse
except ImportError:
    from pymodbus.bit_read_message import ReadCoilsResponse, ReadDiscreteInputsResponse  # type: ignore
    from pymodbus.bit_write_message import WriteMultipleCoilsResponse, WriteSingleCoilResponse  # type: ignore
    from pymodbus.register_read_message import ReadHoldingRegistersResponse  # type: ignore
    from pymodbus.register_write_message import WriteMultipleRegistersResponse  # type: ignore
from pymodbus.constants import Endian

from clickplc.driver import ClickPLC as realClickPLC


class AsyncClientMock(MagicMock):
    """Magic mock that works with async methods."""

    async def __call__(self, *args, **kwargs):
        """Convert regular mocks into into an async coroutine."""
        return super().__call__(*args, **kwargs)

    def stop(self) -> None:
        """Close the connection (2.5.3)."""
        ...

class ClickPLC(realClickPLC):
    """A version of the driver replacing remote communication with local storage for testing."""

    def __init__(self, address, tag_filepath='', timeout=1):
        self.tags = self._load_tags(tag_filepath)
        self.active_addresses = self._get_address_ranges(self.tags)
        self.client = AsyncClientMock()
        self._coils = defaultdict(bool)
        self._discrete_inputs = defaultdict(bool)
        self._registers = defaultdict(bytes)
        self._detect_pymodbus_version()
        if self.pymodbus33plus:
            self.client.close = lambda: None
        self.bigendian = Endian.BIG if self.pymodbus35plus else Endian.Big  # type: ignore[attr-defined]
        self.lilendian = Endian.LITTLE if self.pymodbus35plus else Endian.Little  # type: ignore[attr-defined]

    async def _request(self, method, *args, **kwargs):
        if method == 'read_coils':
            address, count = args
            return ReadCoilsResponse([self._coils[address + i] for i in range(count)])
        if method == 'read_discrete_inputs':
            address, count = args
            return ReadDiscreteInputsResponse([self._discrete_inputs[address + i]
                                               for i in range(count)])
        elif method == 'read_holding_registers':
            address, count = args
            return ReadHoldingRegistersResponse([int.from_bytes(self._registers[address + i],
                                                                byteorder='big')
                                                 for i in range(count)])
        elif method == 'write_coil':
            address, data = args
            self._coils[address] = data
            return WriteSingleCoilResponse(address, data)
        elif method == 'write_coils':
            address, data = args
            for i, d in enumerate(data):
                self._coils[address + i] = d
            return WriteMultipleCoilsResponse(address, data)
        elif method == 'write_registers':
            address, data = args
            for i, d in enumerate(data):
                self._registers[address + i] = d
            return WriteMultipleRegistersResponse(address, data)
        return NotImplementedError(f'Unrecognised method: {method}')
