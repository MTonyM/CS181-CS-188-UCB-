# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def isTerminal(self, state, depth):
        return state.isWin() or state.isLose() or depth == self.depth * state.getNumAgents()

    def isMaxAgent(self, state, depth):
        return depth % state.getNumAgents() == 0

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 1)
    """

    def maxValue(self, state, depth, agentIndex):
        val = [self.value(state.generateSuccessor(agentIndex, action), depth + 1) for action in state.getLegalActions(agentIndex)]
        return max(val)

    def minValue(self, state, depth, agentIndex):
        val = [self.value(state.generateSuccessor(agentIndex, action), depth + 1) for action in state.getLegalActions(agentIndex)]
        return min(val)

    def value(self, state, depth):
        if self.isTerminal(state, depth):
            return self.evaluationFunction(state)
        if self.isMaxAgent(state, depth):
            return self.maxValue(state, depth, depth % state.getNumAgents())
        else:
            return self.minValue(state, depth, depth % state.getNumAgents())

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        var = [self.value(gameState.generateSuccessor(0, action), 1) for action in gameState.getLegalActions(0)]
        i = var.index(max(var))
        return gameState.getLegalActions(0)[i]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha, beta = -1000000.0, 1000000.0
        ret = self.value(gameState, 0, 0, alpha, beta)
        return ret[1]

    def maxValue(self, state, depth, agentIndex, alpha, beta):
        vvv = -1000000.0
        act = None
        for action in state.getLegalActions(agentIndex):
            succ = state.generateSuccessor(agentIndex, action)
            val = self.value(succ, depth+1, agentIndex, alpha, beta)
            if val[0] > vvv:
                vvv = val[0]
                act = action
            if vvv > beta:
                return (vvv ,act)
            alpha = max(alpha, vvv)
        return (vvv, act)

    def minValue(self, state, depth, agentIndex, alpha, beta):
        vvv = 1000000.0
        act = None
        for action in state.getLegalActions(agentIndex):
            succ = state.generateSuccessor(agentIndex, action)
            val = self.value(succ, depth+1, agentIndex, alpha, beta)
            if val[0] < vvv:
                vvv = val[0]
                act = action
            if vvv < alpha:
                return (vvv ,act)
            beta = min(beta, vvv)
        return (vvv, act)

    def value(self, state, depth, agentIndex, alpha, beta):
        if self.isTerminal(state, depth):
            return self.evaluationFunction(state), None
        if (depth) % state.getNumAgents() == 0:
            # print('Max:'+str((alpha,beta)))
            return self.maxValue(state, depth, (depth) % state.getNumAgents(), alpha, beta)
        else:
            # print('min:'+str((alpha,beta)))
            return self.minValue(state, depth, (depth) % state.getNumAgents(), alpha, beta)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        ret = self.value(gameState, 0)
        return ret[1]

    def maxValue(self, state, depth, agentIndex):
        vals = [self.value(state.generateSuccessor(agentIndex, action), depth + 1)[0] for action in state.getLegalActions(agentIndex)]
        act = state.getLegalActions(agentIndex)[vals.index(max(vals))]
        return max(vals), act

    def meanValue(self, state, depth, agentIndex):
        vals = [self.value(state.generateSuccessor(agentIndex, action), depth + 1)[0] for action in state.getLegalActions(agentIndex)]
        return (sum(vals)/len(vals)), None

    def value(self, state, depth):
        if self.isTerminal(state, depth):
            return self.evaluationFunction(state), None
        if (depth) % state.getNumAgents() == 0:
            return self.maxValue(state, depth, (depth) % state.getNumAgents())
        else:
            return self.meanValue(state, depth, (depth) % state.getNumAgents())

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 4).

      DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newCapsules = currentGameState.getCapsules()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    score = currentGameState.getScore()
    capDists = [manhattanDistance(newPos, capPos) for capPos in newCapsules]
    foodDists = [manhattanDistance(newPos, foodPos) for foodPos in newFood]
    ghostDists = [manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates]
    if max(newScaredTimes) > 0:
        # print('fight with ghost')
        return score + 1*max(newScaredTimes)/(ghostDists[newScaredTimes.index(max(newScaredTimes))] + 1)

    if len(capDists) != 0:
        # if min(ghostDists) <= min(capDists):
        # print('seek for caps')
        return score - min(capDists)

    if min(ghostDists) < 2:
        # print('run!')
        return -1000000.0

    if min(foodDists) < 1:
        # print('food!')
        return score

    return score + 1*min(foodDists)

# Abbreviation
better = betterEvaluationFunction

