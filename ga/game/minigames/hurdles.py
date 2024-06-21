import random

from .minigame import Minigame, PlayerAction

from typing import List, Dict


# translated from https://github.com/CodinGame/SummerChallenge2024Olymbits/blob/main/src/main/java/com/codingame/game/mini/HurdleRace.java
class HurdlesGame(Minigame):
    def __init__(self):
        super().__init__("hurdles")
        self.map:          str         = ""
        self.positions:    List[int]   = self._filled_array(0)
        self.stun_timers:  List[int]   = self._filled_array(0)
        self.dead:         List[bool]  = self._filled_array(False)
        self.jumped:       List[bool]  = self._filled_array(False)
        self.finished:     List[int]   = self._filled_array(-1)
        self.rank:         int         = 0
    

    def _reset(self):
        # reset states
        for i in range(3):
            self.positions[i] = 0
            self.stun_timers[i] = 0
            self.finished[i] = -1
            self.rank = 0
            self.jumped[i] = False
        
        # generate new map information
        start_stretch = 3 + random.randrange(5)
        hurdles = 3 + random.randrange(4)
        length = 30  # const: length of map
        sb = ""  # python equivalent of StringBuilder

        # generate new map
        sb += '.' * start_stretch
        for i in range(hurdles):
            sb += "#..."
            if (random.randint(0,1)):
                sb += "."
        while (len(sb) < length):
            sb += "."
        self.map = sb[0:length-1] + "."
    

    def _get_gpu(self):
        return self.map
    

    def _fill_registers(self):
        return self.positions + self.stun_timers
    

    def _tick(self, player_actions):
        maxX = len(self.map) - 1
        countFinishes = 0

        for i in range(3):
            self.jumped[i] = False

            action = player_actions[i]
            if action is None or action == PlayerAction.ERROR:
                self.dead[i] = True
                continue

            if self.stun_timers[i] > 0:
                self.stun_timers[i] -= 1
                continue
            
            if self.finished[i] > -1:
                continue
            
            moveBy = 0
            jump = False

            if action == PlayerAction.DOWN:
                moveBy = 2
            elif action == PlayerAction.LEFT:
                moveBy = 1
            elif action == PlayerAction.RIGHT:
                moveBy = 3
            elif action == PlayerAction.UP:
                moveBy = 2
                jump = True
                self.jumped[i] = True
            else:
                # python allows arrays of any type, so this extra check is
                # rather necessary, just in case
                raise TypeError(f"Unknown action {repr(action)}")
            
            for x in range(moveBy):
                self.positions[i] = min(maxX, self.positions[i] + 1)
                if self.map[self.positions[i]] == '#' and not jump:
                    self.stun_timers[i] = 2  # stun
                    break
                if self.positions[i] == maxX and self.finished[i] == -1:
                    self.finished[i] = self.rank
                    countFinishes += 1
                    break
                jump = False
        self.rank += countFinishes
    

    def _is_game_over(self):
        count = 0
        for i in range(3):
           #if self.finished[i] > -1 and self.get_const('EARLY_RACE_END'):
            if self.finished[i] > -1:
                return True
            if self.finished[i] > -1 or self.dead[i]:
                count += 1
        return count >= 2
    

    def _get_rankings(self):
       #if (self.get_const('EARLY_RACE_END')):
        if True:
            score_by_player: Dict[int, float] = {}
            for i in range(3):
                if self.dead[i]:
                    score_by_player[i] = -1.0
                else:
                    score_by_player[i] = float(self.positions[i])
            return self._create_rankings(score_by_player)
        
        rankings = []
        for i in range(3):
            if self.finished[i] == -1:
                rankings[i] = self.rank
            else:
                rankings[i] = self.finished[i]
        return rankings
