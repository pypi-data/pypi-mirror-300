import typing

import numpy as np
from MrKWatkins.OakAsm.IO.ZXSpectrum.Z80Snapshot import Z80SnapshotFormat  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum import ZXSpectrum as CSharpZXSpectrum  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.Screen import ScreenConverter  # noqa
from System.IO import File  # noqa


class ZXSpectrum:
    def __init__(self, zx=CSharpZXSpectrum.Create48k()):
        self._zx = zx

    def load_snapshot(self, path: str) -> None:
        file = File.OpenRead(path)
        try:
            snapshot = Z80SnapshotFormat.Instance.Read(file)
            self._zx.LoadSnapshot(snapshot)
        finally:
            file.Dispose()

    def set_program_counter(self, address: int) -> None:
        self._zx.Cpu.Registers.PC = address

    def get_rgb24_screenshot(self) -> np.ndarray[typing.Any, np.dtype[np.float64]]:
        rgb24 = bytes(self._zx.GetRgb24Screenshot())
        image_array = np.frombuffer(rgb24, dtype=np.uint8)
        return image_array.reshape((192, 256, 3))

    def execute_frames(self, frames: int = 1) -> None:
        self._zx.ExecuteFrames(frames)
