#!/bin/python3 
from Agent import Agent
from EnvState import Reversi

from typing import Callable
from copy import deepcopy
from random import choice, seed
from math import sqrt

class HMCTSNode:
    def __init__(self, parent, aid : int) -> None:
        self.parent : HMCTSNode = parent
        self.children : dict[tuple, HMCTSNode] = dict()
        self.aid = aid # The agent that made the preceding action
        
        self.Q : float = 0.0 # Expected reward for agent with aid (agent id)
        self.N : float = 0.0 # Times this node has been explored 
        self.P : float = 0.0 # Policy (How promissing this node looks for agent with aid)

def StochasticHeuristic(S : Reversi) -> tuple[dict[tuple, float], list[float]]:
    policy : dict[tuple, float] = dict([(action, 1.0) for action in S.legal])
    values : list[float] = [0.0 for _ in range(S.PLAYER_COUNT)]
    
    simulacra = deepcopy(S)
    seed()
    while len(simulacra.legal) > 0:
        simulacra.act(choice(list(simulacra.legal)))
    
    values[simulacra.result()] = 1.0
    return policy, values

class HeuristicMonteCarloTreeSearch(Agent):
    def __init__(self, environment: Reversi, name: str = "Agent", exploration_quota : int = 1042, heuristic : Callable[[Reversi], tuple[dict[tuple, float], list[float]]] = StochasticHeuristic) -> None:
        super().__init__(environment, name)
        self.exploration_quota : int = exploration_quota
        
        self.root : HMCTSNode = HMCTSNode(None, -1)
        self.heuristic = heuristic

    def notify(self) -> None:
        if self.environment.last_action in self.root.children:
            self.root = self.root.children[self.environment.last_action]
        else: 
            self.root = HMCTSNode(None, self.environment.prev_player)
        return super().notify()

    def deliberate(self) -> None:
        for _ in range(self.exploration_quota):
            self.__treesearch()
        evaluations = dict([(action, self.root.children[action].Q) for action in self.root.children])
        self.decided_action = max(evaluations, key=evaluations.get)
        return super().deliberate()

    def act(self) -> tuple:
        self.root = self.root.children[self.decided_action] 
        self.root.parent = None # Orphaning the new root node. Save memory by droping unneeded reference 
        self.environment.act(self.decided_action)
        return super().act()

    def __treesearch(self): 
        leaf, state = self.__selection()
        self.__expansion(leaf, state)
        values = self.__evaluation(leaf, state) 
        self.__backpropagation(leaf, values)

    def __selection(self) -> tuple[HMCTSNode, Reversi]:
        node = self.root
        state = deepcopy(self.environment)
        while len(node.children) > 0: # While this node has been passed at least once 
            upper_bounds : dict[tuple, float] = dict([(action, HeuristicMonteCarloTreeSearch.UCB(node.children[action])) for action in node.children])
            best = max(upper_bounds, key=upper_bounds.get)
            node = node.children[best]
            state.act(best)
        return node, state 

    def __expansion(self, leaf : HMCTSNode, state : Reversi) -> None:
        leaf.children = dict([(action, HMCTSNode(leaf, state.player)) for action in state.legal])

    def __evaluation(self, leaf : HMCTSNode, state : Reversi) -> list[float]: 
        policy, values = self.heuristic(state)
        for action in policy: 
            leaf.children[action].P = policy[action]
        
        return values
    
    def __backpropagation(self, leaf : HMCTSNode, values : list[float]):
        node = leaf 
        while node != None: 
            node.Q = (node.Q * node.N + values[node.aid])/ (node.N + 1)
            node.N += 1.0
            node = node.parent

    @staticmethod 
    def UCB(node : HMCTSNode, C : float = sqrt(2)):
        return node.Q + C * node.P * ( sqrt(node.parent.N) / (1 + node.N) )
    
