import sys
import enum
from matplotlib import pyplot as plt

from typing import List, Dict, Any, Optional


class PlayerAction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    # special error case
    ERROR = -1

    @classmethod
    def list_values(cls) -> List[int]:
        return list(map(lambda a: a.value, cls))

class Minigame:
    def __init__(self, name: str):
        # save metadata
        self.__name = name
        # init other data (used for resetting (duh))
        self.should_reset:  bool  = False
        self.resetting:     bool  = False
        # check for all funcs
        for attr in ['_reset', '_get_gpu', '_fill_registers', '_tick', '_is_game_over', '_get_rankings']:
            if not hasattr(self, attr):
                print(f"!! Warning: Minigame {name} does not implement {attr}", file=sys.stderr)
    
    @property
    def name(self) -> str:
        return self.__name
    

    def reset(self) -> None:
        """ Generate the GPU for this game step. """
        if not hasattr(self, '_reset'):
            raise NotImplementedError("Games must override _reset()")
        return getattr(self, '_reset')()
    

    def get_gpu(self) -> str:
        """ Generate the GPU for this game step. """
        if not hasattr(self, '_get_gpu'):
            raise NotImplementedError("Games must override _get_gpu()")
        return getattr(self, '_get_gpu')()
    

    def fill_registers(self) -> List[int]:
        """ Generate the registers for this game step. """
        if not hasattr(self, '_fill_registers'):
            raise NotImplementedError("Games must override _fill_registers()")
        regs = getattr(self, '_fill_registers')()
        while len(regs) < 7: regs.append(0)
        return regs
    

    def tick(self, player_actions: List[PlayerAction]) -> None:
        """ Updates this game state with the actions taken by players. """
        if not hasattr(self, '_tick'):
            raise NotImplementedError("Games must override _tick()")
        return getattr(self, '_tick')(player_actions)
    

    def is_game_over(self) -> bool:
        """ Determines if the game is over in its current state. """
        if not hasattr(self, '_is_game_over'):
            raise NotImplementedError("Games must override _is_game_over()")
        return getattr(self, '_is_game_over')()
    

    def get_rankings(self) -> List[int]:
        """ Determines if the game is over in its current state. """
        if not hasattr(self, '_get_rankings'):
            raise NotImplementedError("Games must override _get_rankings()")
        return getattr(self, '_get_rankings')()
    

    def _filled_array(self, value: Any, length: Optional[int] = ...) -> List:
        """
        Helper method to initialize a list filled with a certain value.
        Argument `length` will default to the number of players, :const:`3`.
        """
        if length is ...:
            length = 3  # n_players
        if length < 0:
            raise ValueError("Cannot instantiate array of less than 0 items")
        return [ value for _ in range(length) ]
    

    def _create_rankings(self, score_by_player: Dict[int, float]) -> List[int]:
        """ Helper method for ranking players based on their scores. """
        rankings: List[int] = [ -1 for P in range(3) ]
        entries = score_by_player.items()
        # sort by score, descending
        sorted_entries = list(sorted(
            score_by_player.items(),
            key=lambda e: e[1],
            reverse=True))
        
        rank = 0
        lastRank = 0
        lastScore = None

        # i really, really dont like this code, but this is a near-direct
        # translation of the java version. if that's what the game servers are
        # using, then that's what we will use.
        for (player, score) in sorted_entries:
            currentRank = rank
            if (lastScore is not None and lastScore == score):
                currentRank = lastRank
            lastRank = currentRank

            rankings[player] = currentRank
            
            rank += 1
            lastScore = score
        
        return rankings
