import random
from typing import Union


class LifeOneLine:
    """
    LifeOneLine class for iteratively progressing a ruleset for Conway's Game of Life to generate rhythmic triggers
    for note events.
    """
    def __init__(self, max_size: Union[int, None] = None, initial_state: Union[list, None] = None):
        """
        Initialization for LifeOneLine class.
        :param max_size: int || None
        :param initial_state: list || None
        """
        if initial_state is None:
            self.initial_state = self.generate_random_state(max_size)
            self.max_size = max_size
        else:
            self.initial_state = initial_state
            self.max_size = len(self.initial_state)
        self.grid = self.initial_state

    def run(self, no_of_generations: int = 1):
        """
        Runs the game of Life through a number of generations.
        :param no_of_generations: int
        :return: None
        """
        i = 0
        while i < no_of_generations:
            i += 1
            self.grid = self.apply_rules()

    def apply_rules(self):
        """
        Applies some simplistic logic rules to the game.
        :return: list
        """
        next_state = []
        for i in range(self.max_size):
            total = self.grid[(i - 1) % self.max_size] + self.grid[i % self.max_size] + self.grid[
                (i + 1) % self.max_size]
            if self.grid[i] == 1:
                if total == 3 or total == 1:
                    next_state.append(0)
                if total == 2:
                    next_state.append(1)
            else:
                if total == 0 or total == 2:
                    next_state.append(1)
                else:
                    next_state.append(0)

        return next_state

    def generate_random_state(self, max_size: Union[int, None] = None):
        """
        Constructor function that generates a random state to initialize the first generation.
        :param max_size: int || None
        :return: list
        """
        if max_size is None:
            max_size = self.max_size

        first_generation = [random.choice([0, 1]) for _ in range(max_size)]
        random.shuffle(first_generation)
        return first_generation

    def __str__(self):
        """
        Class override for str(instance)
        :return: str
        """
        return str(self.grid)

    def __repr__(self):
        """
        Class override for representation of LifeOneLine
        :return: str
        """
        return '<{0}.{1} object at {2} || {3}>'.format(
            type(self).__module__, type(self).__qualname__, hex(id(self)), self.__str__())


if __name__ == '__main__':
    life = LifeOneLine(8, initial_state=None)
    life.run(5)
    life.run(1)

    life2 = LifeOneLine(max_size=None, initial_state=[1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0])
    life2.run(20)
