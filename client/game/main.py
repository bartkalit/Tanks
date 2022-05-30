import multiprocessing as mp
from client.game.src.core.screen import Screen
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
statistic = {'0': 0, '1': 0}


def simulation():
    screen = Screen()
    return screen.new_game()


def info(num_of_sim, iter):
    bar_size = 10
    progress = int((iter / num_of_sim) * bar_size) + 1
    result = "["
    for _ in range(progress):
        result += "*"
    for _ in range(bar_size - progress):
        result += "."
    result += "] " + str(statistic)
    print(result)


if __name__ == "__main__":
    num_of_simulations = 20
    for i in range(num_of_simulations):
        result = simulation()
        for winner in result:
            statistic[str(winner)] += 1
        info(num_of_simulations, i)