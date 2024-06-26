import numpy as np
import abc
import util
from game import Agent, Action


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)

        successor_game_state = current_game_state.generate_successor(action=action)
        board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score

        "*** YOUR CODE HERE ***"
        legal_agent_actions = successor_game_state.get_opponent_legal_actions()
        successor_1_game_state = successor_game_state.generate_successor(agent_index=1, action=legal_agent_actions[0])
        # Collect legal moves and successor states
        legal_moves = successor_1_game_state.get_agent_legal_actions()
        # Choose one of the best actions
        scores = [successor_1_game_state.generate_successor(action=action).score for action in legal_moves]
        if scores:
            return max(scores)
        return -1


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        """*** YOUR CODE HERE ***"""
        # util.raiseNotDefined()
        # Initialize the best value and best action
        best_value = -np.inf
        best_action = None

        # Get all legal actions for the agent (agent_index=0)
        legal_actions = game_state.get_legal_actions(agent_index=0)

        for action in legal_actions:
            # Generate the successor game state for each action
            successor = game_state.generate_successor(agent_index=0, action=action)

            # Evaluate the successor state using the minimax function
            value = self.minmax(successor, self.depth, maximizing_player=False)

            # Update the best action if a better value is found
            if value > best_value:
                best_value = value
                best_action = action

        return best_action

    def minmax(self, state, depth, maximizing_player):
        if depth == 0:
            return self.evaluation_function(state)
        if maximizing_player:
            value = -np.inf
            legal_moves = state.get_agent_legal_actions()
            for action in legal_moves:
                successor = state.generate_successor(agent_index=0, action=action)
                value = max(value, self.minmax(successor, depth, False))
            return value
        # minimizing player
        else:
            value = np.inf
            legal_moves = state.get_opponent_legal_actions()
            for action in legal_moves:
                successor = state.generate_successor(agent_index=1, action=action)
                value = min(value, self.minmax(successor, depth - 1, True))
            return value





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        best_value = -np.inf
        best_action = None

        # Get all legal actions for the agent (agent_index=0)
        legal_actions = game_state.get_legal_actions(agent_index=0)

        for action in legal_actions:
            # Generate the successor game state for each action
            successor = game_state.generate_successor(agent_index=0, action=action)

            # Evaluate the successor state using the minimax function
            value = self.alphaBeta(successor, self.depth,-np.inf, np.inf, maximizing_player=False)

            # Update the best action if a better value is found
            if value > best_value:
                best_value = value
                best_action = action

        return best_action

    def alphaBeta(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluation_function(state)
        if maximizing_player:
            value = -1
            legal_moves = state.get_agent_legal_actions()
            for action in legal_moves:
                successor = state.generate_successor(agent_index=0, action=action)
                value = max(value, self.alphaBeta(successor, depth, alpha, beta, False))
                alpha = max(alpha, value)
                if value >= beta:
                    break
            return value
        # minimizing player
        else:
            value = np.inf
            legal_moves = state.get_opponent_legal_actions()
            for action in legal_moves:
                successor = state.generate_successor(agent_index=1, action=action)
                value = min(value, self.alphaBeta(successor, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if value <= alpha:
                    break
            return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        best_value = -np.inf

        # Get all legal actions for the agent (agent_index=0)
        legal_actions = game_state.get_legal_actions(agent_index=0)
        best_action = legal_actions[0]

        for action in legal_actions:
            # Generate the successor game state for each action
            successor = game_state.generate_successor(agent_index=0, action=action)

            # Evaluate the successor state using the minimax function
            value = self.expectiMax(successor, self.depth, maximizing_player=False)

            # Update the best action if a better value is found
            if value > best_value:
                best_value = value
                best_action = action

        return best_action

    def expectiMax(self, state, depth, maximizing_player):
        if depth == 0:
            return self.evaluation_function(state)
        if maximizing_player:
            value = -np.inf
            legal_moves = state.get_agent_legal_actions()
            for action in legal_moves:
                successor = state.generate_successor(agent_index=0, action=action)
                value = max(value, self.expectiMax(successor, depth, False))
            return value
        # minimizing player
        else:
            legal_moves = state.get_opponent_legal_actions()
            scores = [self.expectiMax(state.generate_successor(agent_index=1, action=action), depth - 1, True) for action in legal_moves]
            if scores:
                return np.mean(scores)
            return -np.inf




def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    # Define the weight matrix
    weight_matrix = np.array([
        [1000, 80, 30, 20],
        [10, 5, 4, 3],
        [1, 1, 0.1, 0.1],
        [1, 0.1, 0.03, 0.01]
    ])

    if current_game_state.max_tile >= 1024:
        weight_matrix = np.array([
            [1000, 80, 50, 50],
            [3, 3, 4, 10],
            [1, 1, 5, 5],
            [1, 0.1, 1, 1]
        ])
    # Get the current board
    board = current_game_state.board

    # Calculate the weighted sum
    weighted_sum = np.sum(board * weight_matrix)
    penalty_max = 0
    if board[0][0] != current_game_state.max_tile:
        penalty_max = -100 * current_game_state.max_tile ** 2

    if current_game_state.max_tile >= 512 :
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i, j] == 0:
                    penalty_max += 150

    second_high = np.partition(board.flatten(), -2)[-2]
    if board[0][1] != second_high:
        penalty_max += -20 * second_high ** 2

    # Smoothness penalty (adjacent tiles with similar values are better)
    smoothness_penalty = 0
    for i in range(board.shape[0]):
        for j in range(board.shape[1] - 1):
            if board[i, j] == 0 or board[i, j + 1] == 0:
                continue
            smoothness_penalty -= abs(board[i, j] - board[i, j + 1])
    # for j in range(board.shape[0]):
    #     for i in range(board.shape[1] - 1):
    #         if board[i, j] == 0 or board[i + 1, j] == 0:
    #             continue
    #         smoothness_penalty -= abs(board[i, j] - board[i + 1, j])

    monotonicity_penalty = 0
    for i in range(board.shape[0]):
        for j in range(board.shape[1] - 1):
            if board[i, j] == 0 or board[i, j + 1] == 0:
                continue
            if board[i, j] < board[i, j + 1]:
                monotonicity_penalty -= (board[i, j + 1] - board[i, j])

    for j in range(board.shape[0]):
        for i in range(board.shape[1] - 1):
            if board[i + 1, j] == 0 or board[i, j] == 0:
                continue
            if board[i, j] < board[i + 1, j]:
                monotonicity_penalty -= (board[i + 1, j] - board[i, j])

    # Combine all factors into the final score
    score = weighted_sum + smoothness_penalty + monotonicity_penalty + penalty_max + current_game_state.score

    return score


# Abbreviation
better = better_evaluation_function
