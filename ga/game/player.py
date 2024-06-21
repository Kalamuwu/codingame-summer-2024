import subprocess
import select
import numpy as np

from .minigames import PlayerAction

from typing import List

# TODO


class Player:
    def __init__(self, executable_path: str, gene_idx: int, player_idx: int, genes: np.array):
        self.executable_path = executable_path
        self.gene_idx = gene_idx
        self.player_idx = player_idx
        self.genes = genes
        self.process: subprocess.Popen = None
    
    def init(self):
        ...

        # open process
        self.process = subprocess.Popen(
            [ self.executable_path ],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL)  # TODO pipe this?
        
        # communicate initial information to process:
        #   line 0:  int player_idx
        #   line 1:  int nGames
        self.process.stdin.write(f'{self.player_idx}\n4\n'.encode('utf-8'))
        self.process.stdin.flush()
        
        # communicate genes
        genes_str = ' '.join(map(str, self.genes)) + '\n'
        self.process.stdin.write(genes_str.encode('utf-8'))
        self.process.stdin.flush()

        # ensure state good
        # this will hang if not enough genes have been input
        stdout = self.process.stdout.readline().decode('utf-8').strip()
        if stdout != "INITIALIZED":
            raise Exception("Not good state!")
    

    def get_response(self, input_lines: List[str]) -> PlayerAction:
        """
        Queries the child process for its response to the current game state.
        """
        # send in game state
        for line in input_lines:
            line += '\n'
            self.process.stdin.write(line.encode('utf-8'))
        self.process.stdin.flush()
        # consume and process stdout
        stdout = self.process.stdout.readline().decode('utf-8').strip()
        if stdout == "UP":
            return PlayerAction.UP
        elif stdout == "DOWN":
            return PlayerAction.DOWN
        elif stdout == "LEFT":
            return PlayerAction.LEFT
        elif stdout == "RIGHT":
            return PlayerAction.RIGHT
        raise KeyError(f"Actor {self.player_idx}, gene index {self.gene_idx}, unknown response '{stdout}'")
    

    def close(self):
        """ Closes the child process. """
        self.process.kill()
