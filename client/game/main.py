import multiprocessing as mp
from client.game.src.core.screen import Screen
import os

statistic = {'0': 0, '1': 0}
# os.environ["SDL_VIDEODRIVER"] = "dummy"


def simulation():
    screen = Screen()
    result = screen.new_game()
    del screen
    return result


def info(num_of_sim, iteration):
    bar_size = 10
    progress = int((iteration / num_of_sim) * bar_size) + 1
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
