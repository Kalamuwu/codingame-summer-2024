import random

from .minigame import Minigame, PlayerAction

from typing import List, Dict


# translated from https://github.com/CodinGame/SummerChallenge2024Olymbits/blob/main/src/main/java/com/codingame/game/mini/RollerSpeedSkating.java
class SkatingGame(Minigame):
    def __init__(self):
        super().__init__("skating")
        self.positions:   List[int]           = self._filled_array(0)
        self.risk:        List[int]           = self._filled_array(0)
        self.dead:        List[bool]          = self._filled_array(False)
        self.directions:  List[PlayerAction]  = [PlayerAction.UP,
                                                 PlayerAction.DOWN,
                                                 PlayerAction.LEFT,
                                                 PlayerAction.RIGHT]
        self.timer:       int                 = 0
    

    def _reset(self):
        for i in range(3):
            self.positions[i] = 0
            self.risk[i] = 0
        random.shuffle(self.directions)
        self.timer = 15


    def _get_gpu(self):
        return ''.join(map(lambda a: a.name[0], self.directions))


    def _fill_registers(self):
        return self.positions + \
               self.risk      + \
               [ self.timer ]


    def _tick(self, player_actions):
        # update player positions
        for i in range(3):
            
            action = player_actions[i]
            if action is None or action == PlayerAction.ERROR:
                self.dead[i] = True
                continue
            
            if (self.risk[i] < 0):
                self.risk[i] += 1
                continue

            idx = self.directions.index(action)
            dx = 1 if idx==0 else 3 if idx==3 else 2
            
            self.positions[i] += dx
            riskValue = idx - 1
            self.risk[i] = max(0, self.risk[i] + riskValue)
        
        # check risks
        for i in range(3):
            if (self.risk[i] < 0):
                continue
            
            # check for player overlaps
            length = 10  # const: track length
            clash = False
            for k in range(3):
                if k == i:  # cant collide with yourself
                    continue
                if ((self.positions[k] % length) == (self.positions[i] % length)):
                    clash = True
                    break
            if clash:
                self.risk[i] += 2
            
            if self.risk[i] >= 5:
                self.risk[i] = -2  # stun
        
        random.shuffle(self.directions)
        self.timer -= 1


    def _is_game_over(self):
        return self.timer <= 0


    def _get_rankings(self):
        score_by_player: Dict[int, float] = {}
        for i in range(3):
            if self.dead[i]:
                score_by_player[i] = -1.0
            else:
                score_by_player[i] = float(self.positions[i])
        return self._create_rankings(score_by_player)
