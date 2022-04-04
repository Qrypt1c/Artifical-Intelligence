# Artifical-Intelligence

## A* Implementation Project
### Description:
This project is a working demonstration of admissible heuristics enabling better path finding performance than Djikstra's algorithm. There were two critical aspects to the project: 
1. Maintain optimality (keep the same path cost as Djikstra's algorithm)
2. Reduce the number of nodes explored (when compared to Djikstra's algorithm).

There were different cost functions associated with the heuristic, so each cost function has a different heuristic that best optimizes the path cost and number of nodes explored. The "intelligence" that is demonstrated in this project does not lean on the computer to develop, but rather a human that determines a set of cases which help guide the computer to the global optimum. In the later projects we begin to see a shift from mostly human intelligence to mostly computer intelligence

## Connect4 AI Project
### Description:
This project is a partially working demonstration of the minimax algorithm and alpha-beta pruning. The goal of this game is to have an AI that can defeat most (if not all) human opponents by looking further into the future of possible decisions. The heuristics used here are not concerned about consistency, but rather attach a quantifiable value that gives the computer a sense of how good a particular game state is. The higher the score is for a particular state, the better it is for the AI to choose the set of moves that lead to that state. In order to reduce computational overhead, alpha-beta pruning is used, which enables the AI to spend more time "searching down the tree" of possible decisions by pruning results that do not align with the Nash Equilibrium

## P3 (Deep Q Learning for Pong)
### Description:
This project is a working demonstration of Deep Q Learning on the Atari game "Pong". There is little to no human involvement in the process of learning the game. Given the millions of frames needed to explore, this project is the ideal candidate for reinforcement learning. The computer is given full autonomy to explore the game and learn the rewards associated with a state-action pair. At the beginning of its training stage, the AI spends its time exploring the environment, but as it approaches the end of its training session, it begins to exploit the knowledge it has gained from exploring earlier.
