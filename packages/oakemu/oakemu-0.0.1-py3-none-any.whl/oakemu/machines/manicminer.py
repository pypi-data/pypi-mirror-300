from MrKWatkins.OakEmu.Machines.ZXSpectrum.Games import ManicMiner as CSharpManicMiner  # noqa

from oakemu.machines.game import Game


class ManicMiner(Game):
    def __init__(self):
        super().__init__(CSharpManicMiner())
