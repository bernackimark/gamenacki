import abc

class Renderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render(self, game_state, players: list) -> None:
        """Render the current game state & player information
        Parameters: game_state: GameState, players: list[Player]"""

    @abc.abstractmethod
    def render_error(self, exc: Exception) -> None:
        """Render an exception"""

    @abc.abstractmethod
    def render_log(self, log) -> None:
        """Render the game log.
        Parameters: log: Log"""
