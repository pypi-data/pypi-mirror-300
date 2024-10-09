import random
import math
import hashlib
import argparse
from abc import ABC, abstractmethod

# import logging
# logging.basicConfig(level=logging.WARNING)
# logger = logging.getLogger('MyLogger')

SCALAR=1/(2*math.sqrt(2.0))

class MCTSState(ABC):
    MOVES=[]
    num_moves=len(MOVES)
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def next_state(self): # 🌟
        ...

    @abstractmethod
    def terminal(self) -> bool: # 🌟
        ...

    @abstractmethod
    def reward(self): # 🌟
        ...

    @abstractmethod
    def __hash__(self): # 🌟
        ...

    def __eq__(self,other):
        if hash(self)==hash(other):
            return True
        return False

    @abstractmethod
    def __repr__(self): # 🌟
        ...

class MCTSNode:
	def __init__(self, state, parent=None):
		self.visits=0
		self.reward=0.0	
		self.state=state
		self.children=[]
		self.parent=parent	
	def add_child(self,child_state):
		child=MCTSNode(child_state,self)
		self.children.append(child)
	def update(self,reward):
		self.reward+=reward
		self.visits+=1
	def fully_expanded(self) -> bool: # 🌟 rewrite
		num_moves = self.state.num_moves
		if len(self.children)==num_moves:
			return True
		return False
	def __repr__(self):
		s="Node; children: %d; visits: %d; reward: %f"%(len(self.children),self.visits,self.reward)
		return s

class MCTS_raw:
    @classmethod
    def UCT_search(cls, budget, root, logger=None, log_freq: int=100):
        for iter in range(int(budget)):
            if logger is not None:
                if iter%log_freq==log_freq-1:
                    logger.info("simulation: %d"%(iter+1))
                    logger.info(root)
            front=cls.tree_policy(root)
            reward=cls.default_policy(front.state)
            cls.backup(front,reward)
        return cls.best_child(root,0)

    @classmethod
    def tree_policy(cls, node):
        while not node.state.terminal():
            if not node.fully_expanded():	
                return cls.expand(node)
            else:
                node=cls.best_child(node,SCALAR)

        # a hack to force 'exploitation' in a game where there are many options, and you may never/not want to fully expand first
        # while not node.state.terminal():
        #     if len(node.children)==0:
        #         return cls.expand(node)
        #     elif random.uniform(0,1)<.5:
        #         node=cls.best_child(node,SCALAR)
        #     else:
        #         if not node.fully_expanded():	
        #             return cls.expand(node)
        #         else:
        #             node=cls.best_child(node,SCALAR)
        return node

    @staticmethod
    def expand(node):
        # 统计所有已有动作
        tried_children=[c.state for c in node.children]
        # 循环直到找到一个未尝试过的新动作
        new_state=node.state.next_state()
        while new_state in tried_children and not new_state.terminal(): # 用hash判断是否in
            new_state=node.state.next_state()
        # 添加新动作
        node.add_child(new_state)
        return node.children[-1]

    #current this uses the most vanilla MCTS formula it is worth experimenting with THRESHOLD ASCENT (TAGS)
    @staticmethod
    def best_child(node,scalar):
        bestscore=0.0
        bestchildren=[]
        for c in node.children:
            exploit=c.reward/c.visits
            explore=math.sqrt(2.0*math.log(node.visits)/float(c.visits))	
            score=exploit+scalar*explore
            if score==bestscore:
                bestchildren.append(c)
            if score>bestscore:
                bestchildren=[c]
                bestscore=score
        return random.choice(bestchildren) if bestchildren != [] else None

    @staticmethod
    def default_policy(state):
        if hasattr(state, 'simulate'):
             state = state.simulate()
        else:
            while not state.terminal():
                state=state.next_state()
        return state.reward()

    @staticmethod
    def backup(node,reward):
        while node!=None:
            node.visits+=1
            node.reward+=reward
            node=node.parent
        return None

class MCTS_explore(MCTS_raw):
    @classmethod
    def tree_policy(cls, node):
        # a hack to force 'exploitation' in a game where there are many options, and you may never/not want to fully expand first
        while not node.state.terminal():
            if len(node.children)==0:
                return cls.expand(node)
            elif random.uniform(0,1)<.5:
                node=cls.best_child(node,SCALAR)
            else:
                if not node.fully_expanded():	
                    return cls.expand(node)
                else:
                    node=cls.best_child(node,SCALAR)
        return node

if __name__=="__main__":
    # Learn from https://github.com/haroldsultan/MCTS.git
    class TESTState(MCTSState):
        NUM_TURNS = 10	
        GOAL = 0
        MOVES=[2,-2,3,-3]
        MAX_VALUE= (5.0*(NUM_TURNS-1)*NUM_TURNS)/2
        num_moves=len(MOVES)
        def __init__(self, value=0, moves=[], turn=NUM_TURNS):
            self.value=value
            self.turn=turn
            self.moves=moves
        def next_state(self):
            nextmove=random.choice([x*self.turn for x in self.MOVES])
            next=TESTState(self.value+nextmove, self.moves+[nextmove],self.turn-1)
            return next
        def terminal(self):
            if self.turn == 0:
                return True
            return False
        def reward(self):
            r = 1.0-(abs(self.value-self.GOAL)/self.MAX_VALUE)
            return r
        def __hash__(self):
            return int(hashlib.md5(str(self.moves).encode('utf-8')).hexdigest(),16)
        def __eq__(self,other):
            if hash(self)==hash(other):
                return True
            return False
        def __repr__(self):
            s="Value: %d; Moves: %s"%(self.value,self.moves)
            return s

    parser = argparse.ArgumentParser(description='MCTS research code')
    parser.add_argument('--num_sims', action="store", required=True, type=int)
    parser.add_argument('--levels', action="store", required=True, type=int, choices=range(TESTState.NUM_TURNS+1))
    args=parser.parse_args()

    test_time = 1000
    score_1 = 0
    score_2 = 0

    best_moves = [-20, 27, -16, 14, 18, -15, -8, 6, -4, -2]

    for i in range(test_time):
        current_node=MCTSNode(TESTState())
        current_node=MCTS_raw.UCT_search(args.num_sims,current_node)
        while current_node.children != []:
            # print("Best Child: %s"%current_node.state)
            current_node = MCTS_raw.best_child(current_node, 0)
        print(current_node.state.moves)
        if abs(current_node.state.moves[-1]) == 2:
            score_1 += 1

    print("----------------------------------")


    for i in range(test_time):
        current_node=MCTSNode(TESTState())
        current_node=MCTS_explore.UCT_search(args.num_sims,current_node)
        while current_node.children != []:
            # print("Best Child: %s"%current_node.state)
            current_node = MCTS_explore.best_child(current_node, 0)
        print(current_node.state.moves)
        if abs(current_node.state.moves[-1]) == 2:
            score_2 += 1

    print("Score 1: ", score_1)
    print("Score 2: ", score_2)
    
    # Command: python src/fastmindapi/algo/tree/mcts.py --num_sims 30000 --levels 8 