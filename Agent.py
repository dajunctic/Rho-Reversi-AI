#!/bin/python3
from EnvState import Reversi 
from random import seed, choice
from copy import deepcopy
from math import log, sqrt
from typing import Callable

from concurrent import futures


class Agent:
    def __init__(self, environment : Reversi, name: str = "Agent") -> None:
        self.decided_action = ()
        self.environment = environment
        self.name = name
    
    def setName(self, name):
        self.name = name

    def deliberate(self) -> None:
        # print("{}'s deliberating".format(self.name))
        pass
   
    # return the action the agent choose and update their internal model of 
    # the environment
    def act(self) -> tuple: 
        return self.decided_action

    # Notify the agent that there has been changes in the 
    # environment brought about by the actions of their agents requiring an internal state change
    def notify(self) -> None:
        pass 

class HumanReversiPlayer(Agent):
    def __init__(self,environment : Reversi, name : str = "Human") -> None:
        super().__init__(environment, name)

    def deliberate(self, choice):
        super().deliberate()
        
        self.decided_action = Reversi.strtoact(choice)
        
        return self.decided_action in self.environment.legal
        
        while True:
            choice = input("Choose action (example A4): ")
            try:
                self.decided_action = Reversi.strtoact(choice)
            except: 
                continue
            if self.decided_action not in self.environment.legal:
                print("Not legal, try again") 
                continue
            else:
                break
    
    def get_agent_type(self):
        return "HUMAN"
    
    def act(self) -> tuple:
        self.environment.act(self.decided_action)
        return super().act()


class DummyAgent(Agent):
    def __init__(self, environment, name: str = "Stochastic") -> None:
        super().__init__(environment, name)

    def deliberate(self) -> None:
        super().deliberate()
        seed()
        self.decided_action = choice(list(self.environment.legal))

    def getType(self):
        return "AI"
    
    def act(self) -> tuple:
        self.environment.act(self.decided_action)
        return super().act()

class NaiveMonteCarlo(Agent): 
    def __init__(self, environment : Reversi, name: str = "Naive Monte Carlo") -> None:
        super().__init__(environment, name)

    def deliberate(self) -> None:
        super().deliberate()
        # print(self.environment)
        scores : dict[tuple, int] = dict([(action, 0) for action in self.environment.legal])
        for action in scores: 
            # print("Evaluating {}".format(Reversi.acttostr(action)))
            for _ in range(512):
                seed()
                simulacra = deepcopy(self.environment) 
                simulacra.act(action)
                while len(simulacra.legal) > 0:
                    simulacra.act(choice(list(simulacra.legal)))
                if simulacra.result() == self.environment.player:
                    scores[action] += 1
                else: 
                    scores[action] -= 1
        self.decided_action = max(scores, key=scores.get)
    
    
    def act(self) -> tuple: 
        self.environment.act(self.decided_action) 
        return super().act()

class MCTSNode:
    def __init__(self, parent, agent_id : int) -> None:
        self.parent : MCTSNode = parent
        self.children : dict[tuple, MCTSNode] = dict()

        self.agent_id = agent_id
        self.N : int = 0
        self.W : int = 0

class MonteCarloTreeSearch(Agent):
    # ROLEOUT_TARGET = 128
    def __init__(self, environment: Reversi, name: str = "Agent", playout_count : int = 128, explore_exploit : float = sqrt(2)) -> None:
        super().__init__(environment, name)
        self.root = MCTSNode(None, -1)

        self.playout_count = playout_count
        self.explore_exploit = explore_exploit

        self.executor = futures.ThreadPoolExecutor()

    def notify(self) -> None:
        if self.environment.last_action in self.root.children: 
            self.root = self.root.children[self.environment.last_action]
        else: 
            self.root = MCTSNode(None, self.environment.prev_player)
        return super().notify()

    def checkLegal(self, choice):
        self.decided_action = Reversi.strtoact(choice)
        
        return self.decided_action in self.environment.legal

    def deliberate(self) -> None:
        super().deliberate()

        for _ in range(self.playout_count): 
            self.__treesearch()
        lcts : dict[tuple, float] = dict([(action, MonteCarloTreeSearch.LCT(self.root.children[action], self.explore_exploit)) for action in self.root.children])
        least_risky = max(lcts, key=lcts.get)
        self.decided_action = least_risky
        
    def get_agent_type(self):
        return "AI"
        
    def act(self) -> tuple:
        self.root = self.root.children[self.decided_action] 
        self.root.parent = None # Orphaning the root node
        self.environment.act(self.decided_action)
        return super().act()

    def __treesearch(self): 
        leaf, state = self.__selection_phase()
        self.__expansion_phase(leaf, state)
        self.__simulation_phase(leaf, state)

    def __selection_phase(self) -> tuple[MCTSNode, Reversi]: 
        node = self.root
        state = deepcopy(self.environment)
        while len(node.children) == len(state.legal):
            if len(node.children) == 0:
                break 
            ucts : dict[tuple, float] = dict([(action, MonteCarloTreeSearch.UCT(node.children[action], self.explore_exploit)) for action in node.children])
            next_edge = max(ucts, key=ucts.get)
            node = node.children[next_edge]
            state.act(next_edge)
        return node, state


    def __expansion_phase(self, leaf : MCTSNode, state : Reversi):
        leaf.children = dict([(action, MCTSNode(leaf, state.player)) for action in state.legal])

    @staticmethod 
    def simulation(state : Reversi, action : tuple) -> int: 
        simulacra = deepcopy(state) 
        simulacra.act(action) 
        while len(simulacra.legal) > 0:
            simulacra.act(choice(list(simulacra.legal)))
        return simulacra.result()

    def __simulation_phase(self, leaf : MCTSNode, state : Reversi):
        if len(leaf.children) == 0:
            self.__backpropagation(leaf, state.result())
            return
        seed()
        results : dict[tuple, futures.Future] = dict()
        for action in leaf.children:
            results[action] = self.executor.submit(MonteCarloTreeSearch.simulation, state, action)
        
        for action in results:
            self.__backpropagation(leaf.children[action], results[action].result())

    def __backpropagation(self, leaf : MCTSNode, winner : int): 
        node = leaf
        while node != None:
            node.N += 1
            if winner == node.agent_id: 
                node.W += 1
            node = node.parent

    @staticmethod 
    def UCT(node : MCTSNode, C : float) -> float: 
        return node.W / node.N + C * sqrt( log(node.parent.N) / node.N )

    @staticmethod 
    def LCT(node : MCTSNode, C : float) -> float:
        return node.W / node.N - C * sqrt( log(node.parent.N) / node.N )
