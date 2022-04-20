import time
import random


class VoteProcessor:
    """
    A class to represent a VoteProcessor, which takes in votes, and tallies them.
    """
    def __init__(self, *selectable_options):
        """
        Initializes the VoteProcessor Class
        :param selectable_options: Tuple of selectable options.
        """
        self.candidates = list(selectable_options)
        self.vote_tallies = {option: 0 for option in selectable_options}

    # @clock
    def on_message(self, message):
        """
        Searches through each candidate in self.candidates and tests to see if they are in message. When true
        adds a vote to the vote tallies, and returns a formatted string of the current results. Else returns None
        :param message: String
        :return: String || None
        """
        message = str(message)
        for candidate in self.candidates:
            try:
                if candidate.lower() in message.lower():
                    print(candidate, message)
                    self.vote_tallies[candidate] += 1
                    return self.display_current_results()
            except TypeError:
                print("Not a string, something went wrong")
                continue
        return None

    # @clock
    def tally_votes(self):
        """
        Tallys the votes and returns the result as a dictionary with the results as a percentage.
        :return: {String of candidate: Float of resulting percentage of votes}
        """
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
        """
        Formats the tallied votes into a legible string.
        :return: String of votes.
        """
        totals = self.tally_votes()
        text = ''
        for key, value in totals.items():
            text += key + ':' + ' {0:.2f}'.format(round(value*100, 2))
            text += '\n'
        return text

    # @clock
    def reset_vote_tallies(self):
        """
        Resets the vote tallies to 0
        :return: None
        """
        print('Resetting vote tallies...')
        for candidate in self.candidates:
            self.vote_tallies[candidate] = 0

    def get_winning_key(self):
        """
        Gets the candidate with the highest vote share as a string.
        :return: String
        """
        max_value = max(self.vote_tallies.values())
        keys = [key for key, value in self.vote_tallies.items() if value == max_value]
        return random.choice(keys)

    def get_winning_key_index(self):
        """
        Gets the index of the candidate with the highest vote share.
        :return: int
        """
        winning_key = self.get_winning_key()
        return self.candidates.index(winning_key)

if __name__ == '__main__':
    new_vote = VoteProcessor('a)', 'b)', 'c)', 'd)', 'e)')
    print(new_vote.vote_tallies, new_vote.candidates)
    for i in range(9):
        print(new_vote.on_message('a)'))
        time.sleep(0.1)
    for i in range(5):
        print(new_vote.on_message('I want b)!'))
        time.sleep(0.1)
    for i in range(3):
        new_vote.on_message('give me an!')
        time.sleep(0.1)
    # for i in range(7):
    #     new_vote.on_message('c) sounds pretty cool')
    #     # time.sleep(1)
    # for i in range(3):
    #     new_vote.on_message('d)')
    #     # time.sleep(1)
    print(new_vote.tally_votes())
    print(new_vote.get_winning_key())
    new_vote.reset_vote_tallies()
    new_vote.display_current_results()











