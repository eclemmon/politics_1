import time
from utility_tools import clock


class Voteprocessor:
    def __init__(self, *selectable_options):
        self.candidates = list(selectable_options)
        self.vote_tallies = {option: 0 for option in selectable_options}

    # @clock
    def on_message(self, message):
        message = str(message)
        for candidate in self.candidates:
            try:
                if candidate.lower() in message.lower():
                    self.vote_tallies[candidate] += 1
                else:
                    pass
            except TypeError:
                print("Not a string, something went wrong")
                continue
        self.display_current_results()

    # @clock
    def tally_votes(self):
        total_votes = sum(self.vote_tallies.values())
        final_results_as_percent = {}
        if total_votes == 0:
            for candidate in self.candidates:
                final_results_as_percent[candidate] = 0
            return final_results_as_percent
        else:
            for candidate in self.candidates:
                final_results_as_percent[candidate] = self.vote_tallies[candidate] / total_votes
            return final_results_as_percent

    # @clock
    def display_current_results(self):
        totals = self.tally_votes()
        print('#####'*5, '\n')
        for key, value in totals.items():
            text = key + ':' + '{0:.2f}'.format(round(value*100, 2))
            print(text)
        print('\n')

    # @clock
    def reset_vote_tallies(self):
        print('Resetting vote tallies...')
        for candidate in self.candidates:
            self.vote_tallies[candidate] = 0


if __name__ == '__main__':
    new_vote = Voteprocessor('a)', 'b)', 'c)', 'd)', 'e)')
    print(new_vote.vote_tallies, new_vote.candidates)
    for i in range(9):
        new_vote.on_message('a)')
        time.sleep(1)
    for i in range(5):
        new_vote.on_message('I want b)!')
        time.sleep(1)
    # for i in range(3):
    #     new_vote.on_message('give me an e)!')
    #     # time.sleep(1)
    # for i in range(7):
    #     new_vote.on_message('c) sounds pretty cool')
    #     # time.sleep(1)
    # for i in range(3):
    #     new_vote.on_message('d)')
    #     # time.sleep(1)

    new_vote.reset_vote_tallies()
    new_vote.display_current_results()










