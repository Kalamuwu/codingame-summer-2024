import random
import math
import numpy as np
from matplotlib import pyplot as plt

from typing import List, Dict

from .minigames import PlayerAction
from .player import Player


def get_medal_name(rank: int) -> str:
    """ Helper method to get the name of a medal scored based on rank. """
    if rank == 0:
        return "GOLD medal"
    elif rank == 1:
        return "SILVER medal"
    elif rank == 2:
        return "BRONZE medal"
    return "pat on the back"


def visualize_gene_frame(frame: np.array, scores: List[int], round_num: int) -> None:
    """
    Opens a new window containing a matplotlib visualization of the given
    genetic frame.
    """
    # create first figure -- gene distribution
    # (will create new window)
    plt.figure()
    # labels + etc
    plt.title(f"Gene distribution -- Round {round_num+1}")
    plt.xlabel('Gene number')
    plt.ylabel('Values')
    
    # color points based on performance -- skip zeros
    best_score = max(scores)
    worst_score = best_score
    for score in scores:
        if score == 0: continue
        worst_score = min(worst_score, score)
    if worst_score == 0:
        print("Nothing to visualize, all scores 0")
        return True
    if best_score == worst_score:  # ZeroDivisionError protection
        best_score = worst_score+1
    dscore = best_score-worst_score
    sorted_players = list(sorted(
        enumerate(scores), key=lambda e: e[1],  # sort by score
        reverse=True  # sort descending
    ))
    top_5_players_idxs = [e[0] for e in sorted_players[:5]]  # get top 5 idxs
    def color_for_score(s):
        # zero-scores are black
        if s[1] < 1:
            return (0.0, 0.0, 0.0)
        # top 5 are blue
        if s[0] in top_5_players_idxs:
            return (0.0, 0.0, 1.0)
        # normalize score
        placing = ((s[1]-worst_score) / dscore)
        # lerp red->green
        return ((1-placing), placing, 0.0)
    colors = list(map(color_for_score, enumerate(scores)))
    
    # generate markers
    for gene_idx,genes in enumerate(frame):
        # all points of this gene will share the same x
        x = [gene_idx]*len(genes)
        plt.scatter(x, genes, c=colors, marker='o')
    
    # show the plot and details
    print("Showing genes graph window.")
    plt.show(block=False)
    print("\nTop genes:")
    top_idx = sorted_players[0][0]
    for gene in frame[:, top_idx]:
        if gene < 0:
            print(f" {gene}")
        else:
            print(f"  {gene}")

    # create second figure -- score distribution
    plt.figure()
    # labels + etc
    plt.title(f"Score distribution -- Round {round_num+1}")
    plt.xlabel('Placement')
    plt.ylabel('Score')
    
    # generate markers
    placement_idx = 0
    for player_idx,score in sorted_players:
        x = [gene_idx]*len(genes)
        plt.bar(placement_idx, score,
                color=color_for_score((player_idx, score)))
        placement_idx += 1
    
    # show the plot and details
    print("Showing score graph window.")
    plt.show(block=False)
    print("\nTop 5 scores:\n  pid  score")
    for idx in top_5_players_idxs:
        print(f"  {str(idx).ljust(4)} {scores[idx]}")

    # wait for input
    try:
        input("\nPausing for inspection... press Enter to continue.")
    except KeyboardInterrupt:
        print("\nExiting.")
        return False
    return True



# TODO dynamically updating pyplot of genetic history



class PlayerSubset:
    def __init__(self,
                 do_debug_printing:  bool,
                 do_info_printing:   bool,
                 players:            List[Player]):
        # save settings
        self.do_debug_printing:  bool            = do_debug_printing
        self.do_info_printing:   bool            = do_info_printing
        self.players:            List[Player]    = players
        # initialize player data arrays
        self.dead:               List[bool]      = [ 0, 0, 0 ]

        # special array for holding medal information, with annotation
        self.medals:  List[List[List[int]]]  = [ [
                [ 0, 0, 0 ] for pidx in range(3)
            ] for midx in range(4)
        ]
        """ self.medals[minigame_idx][player_idx] = [gold, silver, bronze] """
    

    def init_player_processes(self) -> None:
        for player in self.players:
            player.init()
    

    def _score_for_player(self, player_idx: int) -> int:
        """ Helper method to calculate the running score for each player. """
        score = 1
        for minigame_medals in self.medals:
            player_medals = minigame_medals[player_idx]
          # score *= (3 * gold + silver)
            score *= (3 * player_medals[0] + player_medals[1])
        return score


    def is_active(self, player_idx: int) -> bool:
        """
        Returns :const:`True` if the player with index :const:`player_idx` is
        active, or :const:`False` if dead.
        """
        return not self.dead[player_idx]


    def gather_responses(self, input_lines: List[str]) -> List[PlayerAction]:
        """
        Gather responses from all active :class:`Player`s, for the current
        minigame.
        """
        # prepend score information
        score_information = [
            (' '.join(
                map(str, [ self._score_for_player(pidx) ] +
                         self.medals[0][pidx] +
                         self.medals[1][pidx] +
                         self.medals[2][pidx] +
                         self.medals[3][pidx] )))
            for pidx in range(3)
        ]
        input_lines = score_information + input_lines

        if self.do_debug_printing:
            print("Round state:")
            for line in input_lines:
                print(' ', line)

        # gather player responses
        responses = []
        for i in range(3):
            if self.dead[i]:
                responses.append(PlayerAction.ERROR)
                continue
            try:
                response = self.players[i].get_response(input_lines)
                responses.append(response)
            except Exception as e:
                print(f"PlayerManager: Failed to get player {i} action, error:", repr(e))
                print(f"PlayerManager: ... Marking player as DEAD")
                self.dead[i] = True
                responses.append(PlayerAction.ERROR)
        return responses


    def update_medals(self, minigame_idx: int, rankings: List[int]) -> None:
        """
        Updates the medals earned by each player, based on their ranking.
        """
        minigame_medals = self.medals[minigame_idx]
        for i in range(3):
            medal_tier = min(rankings[i], 2)
            minigame_medals[i][medal_tier] += 1
    

    def finalize_scores(self) -> Dict[int, int]:
        return {
            player.gene_idx: self._score_for_player(player.player_idx)
            for player in self.players
        }


class PlayerManager:
    def __init__(self,
                 do_debug_printing:  bool,
                 do_info_printing:   bool,
                 executable_path:    str,
                 n_players:          int,
                 n_genes:            int,
                 visualize_every:    int,
                 rare_mut_chance:    int,
                 top_percent_breed:  float):
        # save settings
        self.do_debug_printing:  bool            = do_debug_printing
        self.do_info_printing:   bool            = do_info_printing
        self.executable_path:    str             = executable_path
        self.n_players:          int             = n_players
        self.n_genes:            int             = n_genes
        self.visualize_every:    int             = visualize_every
        self.rare_mut_chance:    int             = rare_mut_chance
        self.top_percent_breed:  float           = top_percent_breed
        
        # initialize player data arrays
        self.scores:             List[int]       = []
        self.dead:               List[bool]      = []

        # special array for holding gene information, with annotation
        self.gene_history:       List[np.array]  = []
        """ self.gene_history[iteration][gene_idx] = [p0_gene, p1_gene, ...] """
        
        # initialize first set of players
        self.reset()
        if self.do_info_printing:
            print(f"PlayerManager: Initialized with {n_players} players, each with {n_genes} genes.")
    
    
    def _generate_random_gene(self) -> float:
        gene = random.random()  # [0, 1)
        gene = 2 * gene - 1     # [-1, 1)
        gene *= 10.0            # [-10, 10)
        return gene
    
    
    def _generate_random_mutation(self) -> float:
        # normal mutation
        if random.random() > self.rare_mut_chance:
            mul = random.randrange(3)-1  # 33% each -1, 0, 1
            mut = random.random()        # [0, 1)
            mut *= mul                   # 67% chance (-1, 1), 33% chance 0
            return mut
        # rare mutation
        mut = random.random()  # [0, 1)
        mut = 2 * mut - 1      # [-1, 1)
        mut *= 8               # [-8, 8)
        return mut
    

    def choose_3(self) -> PlayerSubset:
        """ Returns a random set of 3 players to play a set of games. """
        random_3_player_idxs = random.sample(range(self.n_players), 3)
        players = [
            Player(
                executable_path  = self.executable_path,
                gene_idx         = player_idx,
                player_idx       = internal_idx,
                genes            = self.gene_history[-1][:, player_idx])
            for internal_idx, player_idx in enumerate(random_3_player_idxs)
        ]
        return PlayerSubset(do_debug_printing = self.do_debug_printing,
                            do_info_printing  = self.do_info_printing,
                            players           = players)
    

    def update_scores(self, scores: Dict[int, int]) -> None:
        """
        Updates the scores for the given players. See
        :meth:`PlayerSubset.finalize_scores`.
        """
        for pix,score in scores.items():
            self.scores[pix] += score
    

    def _append_clean_gene_palette(self) -> None:
        self.gene_history.append(np.zeros((self.n_genes, self.n_players), order='F'))
    

    def reset(self) -> None:
        """
        Resets this :class:`PlayerManager`. Re-initializes random players with
        random genes, for a new evolution sequence.
        """
        # initialize player data arrays
        self.players = [ None for _ in range(self.n_players) ]
        self.gene_history = []
        self._clear_player_metadata()

        # initialize new random genes
        self._append_clean_gene_palette()
        for pidx in range(self.n_players):
            for gidx in range(self.n_genes):
                self.gene_history[-1][gidx][pidx] = self._generate_random_gene()
        
        # # assign genes
        # for player_idx in range(self.n_players):
        #     genes = gene_pop[:, player_idx]
        #     self.players[player_idx] = Player(
        #         self.executable_path, self.n_players,
        #         player_idx, genes)


    def is_active(self, player_idx: int) -> bool:
        """
        Returns :const:`True` if the player with index :const:`player_idx` is
        active, or :const:`False` if dead.
        """
        return not self.dead[player_idx]

# 
#     def _finalize_scores(self) -> Dict[int, int]:
#         """
#         Finalizes game scores and computes points per player.
#         """
#         scores = { i: 1 for i in range(self.n_players) }
#         # for each minigame...
#         for minigame_idx in range(4):
#             minigame_medals = self.medals[minigame_idx]
#             # ...calculate each player's score...
#             for i in range(self.n_players):
#                 if self.dead[i]:
#                     scores[i] = -1
#                     continue
#                 gold, silver, bronze = minigame_medals[i]
#                 score = gold * 3 + silver
#                 # ...and multiply it with this players' other game scores.
#                 scores[i] *= score
#         return scores
    

    def _clear_player_metadata(self) -> None:
        """
        Resets the metadata for each player, for the next round of evolution.
        The metadata cleared is: medals, death state.
        """
        # reset players' metadata arrays
        self.dead    = [ False  for _ in range(self.n_players) ]
        self.scores  = [ 0      for _ in range(self.n_players) ]


    def breed(self, round_num: int) -> bool:
        """
        Breeds the next generation of players.
        **NOTE:** Not currently implemented.
        """
        # sort players by final score
        scores_per_player = dict(enumerate(self.scores))
        sorted_players = list(sorted(
            scores_per_player.items(),
            key=lambda entry: entry[1],
            reverse=True))
        sorted_players = list(map(lambda e: e[0], sorted_players))
        
        # print information from the last iteration
        if self.do_info_printing:
            print('\n' + ("="*40))
            print(f"EVOLTION STEP {round_num+1} COMPLETE")
            if self.do_debug_printing:
                print(" Genes peek, first 5:")
                print(self.gene_history[-1][:5, :])
        
        # visualize gene distribution
        if round_num == 0 or (round_num+1) % self.visualize_every == 0:
            cont = visualize_gene_frame(
                self.gene_history[-1],
                self.scores,
                round_num)
            if not cont:
                print("Not continuing")
                return False
        
        # evolve genes:
        #   1. select top n percent players (ceil)
        top_n = math.ceil(len(sorted_players) * self.top_percent_breed)
        gene_pool_idxs = sorted_players[:top_n]
        #   2. clean palette
        self._append_clean_gene_palette()
        #   3. breed new players:
        for pidx in range(self.n_players):
            #   3a. pick a parent
            parent_idx = gene_pool_idxs[random.randrange(top_n)]
            #   3b. fetch their genes
            parent_genes = self.gene_history[-2][:, parent_idx]
            #   3c. mutate and save each one
            for gidx in range(self.n_genes):
                parent_gene = parent_genes[gidx]
                parent_gene += self._generate_random_mutation()
                self.gene_history[-1][gidx][pidx] = parent_gene
        
        # clear players' metadata, for next round of gameplay and evolution
        self._clear_player_metadata()
        return True
