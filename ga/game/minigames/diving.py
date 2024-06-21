import random

from .minigame import Minigame, PlayerAction

from typing import List, Dict


# translated from https://github.com/CodinGame/SummerChallenge2024Olymbits/blob/main/src/main/java/com/codingame/game/mini/Diving.java
class DivingGame(Minigame):
    def __init__(self):
        super().__init__("diving")
        self.goal:           List[PlayerAction]        = []  # no init
        self.player_inputs:  List[List[PlayerAction]]  = []  # no init
        self.turns_left:     int                       = 0
        self.points:         List[int]                 = self._filled_array(0)
        self.combo:          List[int]                 = self._filled_array(0)
        self.dead:           List[bool]                = self._filled_array(False)


    def _reset(self):
        self.goal.clear()
        self.player_inputs.clear()

        length = 12 + random.randrange(4)
        for i in range(length):
            random_action = random.choice([PlayerAction.UP,
                                           PlayerAction.DOWN,
                                           PlayerAction.LEFT,
                                           PlayerAction.RIGHT])
            self.goal.append(random_action)

        for i in range(3):
            self.points[i] = 0
            self.combo[i] = 0
            self.player_inputs.append([])
        
        self.turns_left = length + 1


    def _get_gpu(self):
        return ''.join(map(lambda a: a.name[0], self.goal))


    def _fill_registers(self):
        return self.points + self.combo


    def _tick(self, player_actions):
        this_goal = self.goal.pop(0)

        for i in range(3):
            
            action = player_actions[i]
            if action is None or action == PlayerAction.ERROR:
                self.dead[i] = True
                continue
            
            if (action == this_goal):
                self.combo[i] += 1
                self.points[i] += self.combo[i]
            else:
                self.combo[i] = 0
            
            self.player_inputs[0].append(action)
        
        self.turns_left = len(self.goal) + 1


    def _is_game_over(self):
        return len(self.goal) == 0
    

    def _get_rankings(self):
        score_by_player: Dict[int, float] = {}
        for i in range(3):
            if self.dead[i]:
                score_by_player[i] = -1.0
            else:
                score_by_player[i] = float(self.points[i])
        return self._create_rankings(score_by_player)
