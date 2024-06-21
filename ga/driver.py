import random
import math
#from tqdm import tqdm
import multiprocessing as mp
from collections import deque

from typing import List, Tuple

from game.game_manager import GameManager
from game.player_manager import PlayerManager, PlayerSubset


def run_games(rounds: int, thread_idx: int, games_per_pop: int,
              do_debug_printing: bool, do_info_printing: bool,
              players_queue: mp.Queue, scores_queue: mp.Queue):
    # play some games
    for game_i in range(games_per_pop):
        # get new set of players and games
        #players = player_manager.choose_3()
        players: PlayerSubset = players_queue.get()
        players.init_player_processes()
        game_manager = GameManager(
            do_debug_printing = do_debug_printing,
            do_info_printing  = do_info_printing,
            player_subset     = players)
        # play a game -- 100 steps per game
        for round_i in range(rounds):
            game_manager.tick()
        # finally, accumulate each player's score
        scores = players.finalize_scores()
        scores_queue.put(scores)

        #player_manager.update_scores(players.finalize_scores())
        # if SETTINGS['PRINT_INFO']:
        #     print(f"Finished game {game_i+1}/{SETTINGS['NUM_GAMES_PER_POP']}".ljust(25),
        #           f"Players {players.players[0].gene_idx} vs",
        #                   f"{players.players[1].gene_idx} vs",
        #                   f"{players.players[2].gene_idx}")


if __name__ == '__main__':

    # tunable settings
    SETTINGS = {
        'EXECUTABLE_PATH':       '/home/kalamari/projects/cg-summer-2024/build/cg-summer-2024',
        'PRINT_DEBUG':           False,
        'PRINT_INFO':            True,
        'PLAYER_COUNT':          128,
        'NUM_GAMES_PER_POP':     4096,
        'THREAD_COUNT':          32,
        'VISUALIZE_EVERY':       20,
        'GENE_COUNT':            16,
        'RARE_MUT_CHANCE':       0.005,  # 0.5%
        'TOP_PERCENT_BREED':     0.10    # 10%
    }
    
    # initialize player manager
    player_manager = PlayerManager(
        do_debug_printing  = SETTINGS['PRINT_DEBUG'],
        do_info_printing   = SETTINGS['PRINT_INFO'],
        executable_path    = SETTINGS['EXECUTABLE_PATH'],
        n_players          = SETTINGS['PLAYER_COUNT'],
        n_genes            = SETTINGS['GENE_COUNT'],
        visualize_every    = SETTINGS['VISUALIZE_EVERY'],
        rare_mut_chance    = SETTINGS['RARE_MUT_CHANCE'],
        top_percent_breed  = SETTINGS['TOP_PERCENT_BREED'])
    
    ctx = mp.get_context('spawn')
    games_per_thread = SETTINGS['NUM_GAMES_PER_POP'] / SETTINGS['THREAD_COUNT']
    games_per_thread = math.ceil(games_per_thread)
    if SETTINGS['PRINT_INFO']:
        total_games = games_per_thread * SETTINGS['THREAD_COUNT']
        print(f"Playing {total_games} games per population.\n")
    
    should_continue = True
    num_rounds = 0
    while should_continue:

        # start processes
        processes: List[Tuple[mp.Process, mp.Queue, mp.Queue]] = []
        for thread_idx in range(SETTINGS['THREAD_COUNT']):

            players_queue = ctx.Queue()
            scores_queue = ctx.Queue()
            
            proc = ctx.Process(target=run_games, args=(
                100, thread_idx, games_per_thread,
                SETTINGS['PRINT_DEBUG'], SETTINGS['PRINT_INFO'],
                players_queue, scores_queue))
            
            for i in range(games_per_thread):
                players_queue.put(player_manager.choose_3())
            
            proc.start()
            processes.append( (proc, players_queue, scores_queue) )
        
        # gather scores
        for thread_idx in range(SETTINGS['THREAD_COUNT']):
            proc, players_queue, scores_queue = processes[thread_idx]
            for i in range(games_per_thread):
                scores = scores_queue.get()
                player_manager.update_scores(scores)
            proc.join()

        # evolve players
        should_continue = player_manager.breed(num_rounds)
        num_rounds += 1
