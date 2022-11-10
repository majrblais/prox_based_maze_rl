from environment.maze import Maze, Render
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

import logging
from enum import Enum, auto

import matplotlib.pyplot as plt
import numpy as np

import models

from gym_maze.envs.generators import SimpleMazeGenerator, RandomMazeGenerator, RandomBlockMazeGenerator, TMazeGenerator, WaterMazeGenerator

logging.basicConfig(format="%(levelname)-8s: %(asctime)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)  # Only show messages *equal to or above* this level


class Test(Enum):
    SHOW_MAZE_ONLY = auto()
    RANDOM_MODEL = auto()
    Q_LEARNING = auto()
    Q_ELIGIBILITY = auto()
    SARSA = auto()
    SARSA_ELIGIBILITY = auto()
    DEEP_Q = auto()
    LOAD_DEEP_Q = auto()
    SPEED_TEST_1 = auto()
    SPEED_TEST_2 = auto()


test = Test.Q_ELIGIBILITY  # which test to run
maze = np.array([
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 1, 1, 1],
    [0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0]
])  # 0 = free, 1 = occupied

maze_gen = RandomBlockMazeGenerator(maze_size=6, obstacle_ratio=0.2)
maze=maze_gen.maze
print(maze)
game = Maze(maze, num_exit=2)


# train using tabular Q-learning and an eligibility trace (aka TD-lambda)
if test == Test.Q_ELIGIBILITY:
    game.render(Render.TRAINING)
    model = models.QTableTraceModel(game)
    h, w, _, _ = model.train(discount=0.90, exploration_rate=0.10, learning_rate=0.10, episodes=50,
                             stop_at_convergence=True)

if test == Test.DEEP_Q:
    game.render(Render.NOTHING)
    model = models.QReplayNetworkModel(game)
    h, w, _, _ = model.train(discount=0.80, exploration_rate=0.10, episodes=maze.size * 10, max_memory=maze.size * 4,
                             stop_at_convergence=True)

print(h)
print(w)

game.render(Render.MOVES)
game.play(model, start_cell=(0, 0))
print("done")
plt.show()  # must be placed here else the image disappears immediately at the end of the program
