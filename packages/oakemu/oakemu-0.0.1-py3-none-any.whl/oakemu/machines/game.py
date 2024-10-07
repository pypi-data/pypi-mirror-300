import abc

from MrKWatkins.OakEmu.Machines.ZXSpectrum.Game import Game as CSharpGame  # noqa

from oakemu.machines.stepresult import StepResult
from oakemu.machines.zxspectrum import ZXSpectrum


class Game(metaclass=abc.ABCMeta):
    def __init__(self, game: CSharpGame):
        game.InitializeAsync().Wait()
        self._game = game
        self._zx = ZXSpectrum(game.Spectrum)

    @property
    def spectrum(self):
        return self._zx

    def start_episode(self) -> None:
        self._game.StartEpisode()

    def execute_step(self, action: str | None) -> StepResult:
        return StepResult(self._game.ExecuteStep(action))

    def get_random_action(self) -> str | None:
        return self._game.GetRandomAction()
