# game.py
# Wrapper class for all four minigames

import sys
import random

from typing import List, Dict, Any

from .player_manager import PlayerManager, PlayerSubset
from .minigames import \
    PlayerAction, Minigame, \
    HurdlesGame, ArcheryGame, SkatingGame, DivingGame


class GameManager:
    def __init__(self,
                 do_debug_printing:  bool,
                 do_info_printing:   bool,
                 player_subset:      PlayerSubset):
        # save settings
        self.do_debug_printing = do_debug_printing
        self.do_info_printing = do_info_printing

        # initialize data
        self.player_subset:   PlayerSubset    = player_subset
        self.resets:          List[int]       = [ 0 for _ in range(4) ]
        self.minigames:       List[Minigame]  = [ HurdlesGame(),
                                                  ArcheryGame(),
                                                  SkatingGame(),
                                                  DivingGame() ]
        
        # initialize games
        for game in self.minigames:
            game.reset()

        # # output game settings
        # if self.do_debug_printing:
        #     longest_k_length = max(map(len, self.settings.keys()))
        #     longest_kv_length = max(map(lambda kv: len(str(kv[0]))+len(str(kv[1])), self.settings.items()))
        #     top_bottom_bar = '=' * (longest_kv_length+6)
        #     print(top_bottom_bar)
        #     print("Initialized Game with settings:")
        #     for k,v in self.settings.items():
        #         k = k.ljust(longest_k_length)
        #         print(f"  {k}  {v}")
        #     print(top_bottom_bar)


    def tick(self):
        """
        Perform a single game step, for all players, for all minigames.
        """
        # check gameovers, if needed
        for i,minigame in enumerate(self.minigames):
            # handle reset, if needed
            minigame.resetting = False
            if (minigame.should_reset):
                minigame.resetting = True
                minigame.reset()
                self.resets[i] += 1
                minigame.should_reset = False
                continue
        
        # generate game state output
        # note: score information is prepended automatically by
        # `PlayerSubset.gather_responses`, so this is simply game output
        output_lines = [
            ((minigame.get_gpu() if not minigame.resetting else 'GAME_OVER') +
            ' ' +
            ' '.join(
                map(str, minigame.fill_registers())))
            for minigame in self.minigames ]
        
        # gather player actions for given gamestate
        actions = self.player_subset.gather_responses(output_lines)
        for minigame in self.minigames:
            minigame.tick(actions)
        
        # handle new gameovers, if needed
        for i,minigame in enumerate(self.minigames):
            if minigame.is_game_over():
                if self.do_debug_printing:
                    print(f"Finished minigame {minigame.name}")
                minigame.should_reset = True
                rankings = self.get_rankings_for(minigame)
                self.player_subset.update_medals(i, rankings)


    def get_rankings_for(self, minigame: Minigame) -> List[int]:
        """
        Wrapper for :meth:`minigame.get_rankings()` to fill-in dead players.
        """
        rankings = minigame.get_rankings()
        for i in range(3):
            if not self.player_subset.is_active(i):
                rankings[i] = 2
        return rankings


# @Singleton
# public class Game {
#     public static int PLAYER_COUNT = 3;
#     public static final int REGISTER_COUNT = 7;
# 
#     public static boolean EARLY_RACE_END = true;
# 
#     @Inject private MultiplayerGameManager<Player> gameManager;
#     @Inject private EndScreenModule endScreenModule;
# 
#     List<MiniGame> minigames;
#     List<Player> players;
#     Random random;
#     int[] resets;
# 
# 
#     public void resetGameTurnData() {
#         players.forEach(Player::reset);
# 
#     }
# 
#     public boolean isGameOver() {
#         return gameManager.getActivePlayers().size() < 2;
#     }
# 
#     public void onEnd() {
#         String[] scoreTexts = new String[players.size()];
#         for (Player p : players) {
#             if (!p.isActive()) {
#                 p.setScore(-1);
#                 scoreTexts[p.getIndex()] = "-";
#             } else {
#                 p.setScore(p.getPoints());
#                 scoreTexts[p.getIndex()] = p.getScoreText();
# 
#             }
#         }
#         int[] scores = players.stream().mapToInt(Player::getScore).toArray();
#         int[][] medals = players.stream().map(Player::getMedalsTotal).toArray(int[][]::new);
# 
#         endScreenModule.setScores(scores, medals);
# 
#         computeMetadata();
#     }
# 
#     private void computeMetadata() {
#         int goldMedals = 0;
#         for (Player p : players) {
#             goldMedals += p.getMedalsTotal()[0];
#         }
#         gameManager.putMetadata("gold_medals", goldMedals);
#     }
# 
# }
