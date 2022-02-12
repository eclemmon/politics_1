import time

# set voting period and resting period
# after 1 second update timer

class Countdown:
    def __init__(self, voting_period, rest_period):
        # Set initial resting period and voting period
        self.init_vote_period = voting_period
        self.init_rest_period = rest_period
        # Set counts to initial values
        self.vote_period_count = self.init_vote_period
        self.rest_period_count = self.init_rest_period
        # Set is_voting_period to false
        self.is_voting_period = False

    def voting_countdown_print(self):
        mins, secs = divmod(self.vote_period_count, 60)
        timeformat = '{:02d}:{:02d} SEND IN YOUR VOTES NOW! \r'.format(mins, secs)
        return timeformat

    def resting_countdown_print(self):
        mins, secs = divmod(self.rest_period_count, 60)
        timeformat = '{:02d}:{:02d} VOTING OPENS SOON! \r'.format(mins, secs)
        return timeformat

    def voting_period(self):
        while self.vote_period_count > 0:
            count = self.voting_countdown_print()
            self.vote_period_count -= 1
            return count
        else:
            self.vote_period_count = self.init_vote_period
            self.resting_period()

    def resting_period(self):
        while self.rest_period_count > 0:
            count = self.resting_countdown_print()
            self.rest_period_count -= 1
            return count
        else:
            self.rest_period_count = self.init_rest_period
            self.voting_period()



if __name__ == '__main__':
    new_countdown = Countdown(10, 5)
    new_countdown.voting_period()

