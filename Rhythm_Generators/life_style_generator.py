import random


class LifeOneLine:
    def __init__(self, max_size=None, initial_state=None):
        if initial_state is None:
            self.initial_state = self.generate_random_state(max_size)
            self.max_size = max_size
        else:
            self.initial_state = initial_state
            self.max_size = len(self.initial_state)
        self.grid = self.initial_state

    def run(self, no_of_generations=1):
        print(self)
        i = 0
        while i < no_of_generations:
            i += 1
            self.grid = self.apply_rules()
            print(self)

    def apply_rules(self):
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

    def generate_random_state(self, max_size=None):
        if max_size is None:
            max_size = self.max_size

        array = [random.choice([0, 1]) for _ in range(max_size)]
        random.shuffle(array)
        return array

    def __repr__(self):
        return str(self.grid)


if __name__ == '__main__':
    life = LifeOneLine(8, initial_state=None)
    life.run(5)
    life.run(1)

    life2 = LifeOneLine(max_size=None, initial_state=[1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0])
    life2.run(20)
