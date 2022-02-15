import time


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
        if self.vote_period_count > 0:
            count = self.voting_countdown_print()
            self.vote_period_count -= 1
            return count
        else:
            # Reset vote count
            self.vote_period_count = self.init_vote_period
            self.is_voting_period = False
            return self.resting_period()

    def resting_period(self):
        if self.rest_period_count > 0:
            count = self.resting_countdown_print()
            self.rest_period_count -= 1
            return count
        else:
            self.rest_period_count = self.init_rest_period
            self.is_voting_period = True
            return self.voting_period()

    def count(self):
        if self.is_voting_period:
            return self.voting_period()
        else:
            return self.resting_period()


if __name__ == '__main__':
    new_countdown = Countdown(10, 5)
    for _ in range(20):
        print(new_countdown.count())

