import abc

from MrKWatkins.OakEmu.Machines.ZXSpectrum.Game import Game as DotNetGame  # noqa
from oakemu.machines.zxspectrum.stepresult import StepResult
from oakemu.machines.zxspectrum.zxspectrum import ZXSpectrum


class Game(metaclass=abc.ABCMeta):
    def __init__(self, game: DotNetGame):
        game.InitializeAsync().Wait()
        self._game = game
        self._zx = ZXSpectrum(game.Spectrum)
        self._actions = frozenset(game.Actions)

    @property
    def spectrum(self) -> ZXSpectrum:
        return self._zx
    
    @property
    def actions(self) -> frozenset[str]:
        return self._actions

    def start_episode(self) -> None:
        self._game.StartEpisode()

    def execute_step(self, action: str | None) -> StepResult:
        return StepResult(self._game.ExecuteStep(action))

    def get_random_action(self) -> str | None:
        return self._game.GetRandomAction()
