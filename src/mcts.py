import math
import random


class MahjongGameState:
    def __init__(self, hand_tiles, discarded_tiles):
        self.hand_tiles = hand_tiles
        self.discarded_tiles = discarded_tiles

    def get_legal_actions(self):
        # 根据当前手牌, 生成所有合法的出牌动作
        legal_actions = []
        # TODO: 实现根据规则生成合法出牌动作的逻辑
        return legal_actions

    def execute_action(self, action):
        # 根据出牌动作更新游戏状态
        # TODO: 实现根据出牌动作更新游戏状态的逻辑
        pass

    def is_terminal(self):
        # 判断游戏是否结束
        # TODO: 实现判断游戏是否结束的逻辑
        pass

    def get_winner(self):
        # 获取游戏的赢家
        # TODO: 实现获取游戏赢家的逻辑
        pass


class MonteCarloTreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visit_count = 0
        self.win_count = 0

    def is_fully_expanded(self):
        # 判断节点是否完全展开
        return len(self.children) == len(self.state.get_legal_actions())

    def select_child(self):
        # 根据UCB算法选择一个子节点
        exploration_factor = 1.4
        best_score = float("-inf")
        best_child = None
        for child in self.children:
            score = child.win_count / child.visit_count + exploration_factor * math.sqrt(
                2 * math.log(self.visit_count) / child.visit_count
            )
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def expand(self):
        # 展开一个未扩展的子节点
        legal_actions = self.state.get_legal_actions()
        for action in legal_actions:
            new_state = self.state.execute_action(action)
            new_node = MonteCarloTreeNode(new_state, self)
            self.children.append(new_node)
        return self.children[0]

    def simulate(self):
        # 随机模拟游戏直到结束, 并返回胜利的玩家
        current_state = self.state
        while not current_state.is_terminal():
            legal_actions = current_state.get_legal_actions()
            action = random.choice(legal_actions)
            current_state = current_state.execute_action(action)
        winner = current_state.get_winner()
        return winner

    def backpropagate(self, winner):
        # 更新该节点及其父节点的访问次数和胜利次数
        self.visit_count += 1
        if winner == "AI":
            self.win_count += 1
        if self.parent:
            self.parent.backpropagate(winner)

    def get_best_action(self):
        # 根据子节点的访问次数选择最优的出牌动作
        best_child = max(self.children, key=lambda child: child.visit_count)
        best_action = best_child.state.get_last_action()
        return best_action


def mcts_search(state, num_iterations):
    root = MonteCarloTreeNode(state)
    for _ in range(num_iterations):
        node = root
        # Selection
        while not node.is_fully_expanded() and not node.state.is_terminal():
            node = node.select_child()
        # Expansion
        if not node.state.is_terminal():
            node = node.expand()
        # Simulation
        winner = node.simulate()
        # Backpropagation
        node.backpropagate(winner)
    return root.get_best_action()


# 示例用法


hand_tiles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
discarded_tiles = []
initial_state = MahjongGameState(hand_tiles, discarded_tiles)
best_action = mcts_search(initial_state, 10000)
