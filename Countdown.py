import time

class Countdown:
    def __init__(self, voting_period, rest_period):
        self.init_seconds = voting_period
        self.seconds = self.init_seconds
        self.init_rest_period = rest_period
        self.rest_period = self.init_rest_period

    def voting_countdown_print(self):
        mins, secs = divmod(self.seconds, 60)
        timeformat = '{:02d}:{:02d} SEND IN YOUR VOTES NOW! \r'.format(mins, secs)
        return timeformat

    def resting_countdown_print(self):
        mins, secs = divmod(self.rest_period, 60)
        timeformat = '{:02d}:{:02d} VOTING OPENS SOON! \r'.format(mins, secs)
        return timeformat

    def voting_period(self):
        while self.seconds > 0:
            self.voting_countdown_print()
            count = self.voting_countdown_print()
            print(count)
            self.seconds -= 1
        else:
            self.seconds = self.init_seconds
            self.resting_period()

    def resting_period(self):
        while self.rest_period > 0:
            count = self.resting_countdown_print()
            print(count)
            self.rest_period -= 1
        else:
            self.rest_period = self.init_rest_period
            self.voting_period()



if __name__ == '__main__':
    new_countdown = Countdown(10, 5)
    new_countdown.voting_period()

