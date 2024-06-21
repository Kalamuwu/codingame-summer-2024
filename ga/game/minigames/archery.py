import random

from .minigame import Minigame, PlayerAction

from typing import List, Dict


# magic numbers extracted from java code
WIND_WEIGHTS = [ 0, 2, 2, 2, 0.5, 0.5, 0.25, 0.25, 0.25, 0.2 ]

# translated from https://github.com/CodinGame/SummerChallenge2024Olymbits/blob/main/src/main/java/com/codingame/game/mini/Archery.java
class ArcheryGame(Minigame):
    def __init__(self):
        super().__init__("archery")
        self.cursors:  List[List[int]]  = []  # list of x,y pairs. init below
        self.wind:     List[int]        = []  # list of directions. no init
        self.arrows:   bool             = False
        self.dead:     List[bool]       = self._filled_array(False)

        # initialize cursors
        for i in range(3):
            self.cursors.append( [0,0] )


    @staticmethod
    def _random_direction():
        """ Helper method to choose a random wind direction, 0-9. """
        rand = random.random()
        # normalize weights to sum to 1
        total = sum(WIND_WEIGHTS)
        b = 1 / total
        weights = list(map(lambda v: v*b, WIND_WEIGHTS))
        # choose index
        cur = 0
        for i in range(len(weights)):
            cur += weights[i]
            if (cur >= rand):
                return i
        return 0

    
    def _reset(self):
        random_sign = lambda: 1 if random.randint(0,1) else -1
        x = (5 + random.randrange(5)) * random_sign()
        y = (5 + random.randrange(5)) * random_sign()
        for cursor in self.cursors:
            cursor[0] = x
            cursor[1] = y
        
        self.wind.clear()
        rounds = 12 + random.randrange(4)
        for i in range(rounds):
            self.wind.append(self._random_direction())
        
        self.arrows = False


    def _get_gpu(self):
        return ''.join(map(str, self.wind))


    def _fill_registers(self):
        return [
            self.cursors[0][0], self.cursors[0][1],
            self.cursors[1][0], self.cursors[1][1],
            self.cursors[2][0], self.cursors[2][1]
        ]


    def _tick(self, player_actions):
        maxDist = 20
        offset = self.wind.pop(0)

        for i in range(3):
            
            action = player_actions[i]
            if action is None or action == PlayerAction.ERROR:
                self.dead[i] = True
                continue
            
            dx = 0
            dy = 0

            if action == PlayerAction.DOWN:
                dy = offset
            elif action == PlayerAction.LEFT:
                dx = -offset
            elif action == PlayerAction.RIGHT:
                dx = offset
            elif action == PlayerAction.UP:
                dy = -offset
            else:
                # python allows arrays of any type, so this extra check is
                # rather necessary, just in case
                raise TypeError(f"Unknown action {repr(action)}")
            
            cursor = self.cursors[i]
            cursor[0] += dx
            cursor[1] += dy

            if cursor[0] >  maxDist: cursor[0] =  maxDist
            if cursor[0] < -maxDist: cursor[0] = -maxDist
            if cursor[1] >  maxDist: cursor[1] =  maxDist
            if cursor[1] < -maxDist: cursor[1] = -maxDist
        
        self.arrows = self.is_game_over()


    def _is_game_over(self):
        return len(self.wind) == 0

    
    def _get_rankings(self):
        score_by_player: Dict[int, float] = {}
        for i in range(3):
            if self.dead[i]:
                score_by_player[i] = -999999 # arbitrarily large negative num
                continue
            cursor = self.cursors[i]
            distance = cursor[0]**2 + cursor[1]**2
            score_by_player[i] = -distance
        return self._create_rankings(score_by_player)
