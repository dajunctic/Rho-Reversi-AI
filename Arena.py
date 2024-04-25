#!/bin/python3 
import EnvState 
import Agent
import threading
from copy import deepcopy
from typing import Callable
from concurrent import futures

from HeuristicMonteCarloTreeSearch import HeuristicMonteCarloTreeSearch

class Arena:
    def __init__(self, env_state: EnvState.Reversi, agents: list[Agent.Agent]) -> None:
        self.__agents_list = agents
        self.__cannonical_state = env_state

        assert env_state.PLAYER_COUNT == len(agents)

    def evaluate(self, print_env : bool = False, print_action : bool = False, show_legal : bool = False) -> None: 
        if print_env: 
            print(self.__cannonical_state)
        if show_legal: 
            print("Legal: {}".format(self.__cannonical_state.legal))
        while len(self.__cannonical_state.legal) > 0:
            edge = ()
            a = self.__agents_list[self.__cannonical_state.player] 
            a.deliberate() 
            edge = a.act()

            for oa in self.__agents_list: 
                if oa is not a: 
                    oa.notify()

            if show_legal: 
                print("Legal: {}".format(self.__cannonical_state.legal))
            if print_env: 
                print(self.__cannonical_state)
            if print_action:
                print("{} played : {}".format(a.name, edge))
        if print_env: 
            print(self.__cannonical_state)
        
        
    def getWinner(self):
        winner = self.__cannonical_state.result()
        if winner < 0: 
            return "None"
        else:
            return self.__agents_list[winner].name

def smart_machine(g : EnvState.Reversi):
    return Agent.MonteCarloTreeSearch(g, "MCTS-1")

def dumb_machine(g : EnvState.Reversi):
    return Agent.DummyAgent(g, "Not smart")

def pure_monte_carlo_tree_search(g : EnvState.Reversi):
    return Agent.MonteCarloTreeSearch(g, "Pure monte carlo tree search")

def heuristic_monte_carlo_tree_search(g : EnvState.Reversi):
    return HeuristicMonteCarloTreeSearch(g, "Heuristic monte carlo tree search")


def contest(SetupGame : Callable[[], EnvState.Reversi], SetupCompetitors : list[Callable[[EnvState.Reversi], Agent.Agent]], batch : int = 16) -> dict[str, int]:
    scoreboard : dict[str, int] = dict()
    for _ in range(batch):
        print("Iteration : {}".format(_ + 1))
        game = SetupGame() 
        agents = [Competitor(game) for Competitor in SetupCompetitors]
        playground = Arena(game, agents)
        victor = playground.evaluate(print_action=True) 
        if victor not in scoreboard: 
            scoreboard[victor] = 1
        else: 
            scoreboard[victor] += 1
    return scoreboard

if __name__ == "__main__":
    queue = [] 
    results = []
    with futures.ThreadPoolExecutor() as executor:
        for _ in range(8):
            queue.append( executor.submit( contest, Agent.Reversi, [ pure_monte_carlo_tree_search, heuristic_monte_carlo_tree_search ], 2 ) )
        for _ in range(8):
            queue.append( executor.submit( contest, Agent.Reversi, [ heuristic_monte_carlo_tree_search, pure_monte_carlo_tree_search ], 2 ) )

        for f in queue:
            results.append(f.result())
    for r in results: 
        print(r)

