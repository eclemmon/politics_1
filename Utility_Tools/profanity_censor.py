from better_profanity import profanity


class Censor:
    def __init__(self, censor_level=0):
        self.censor_level = censor_level
        if self.censor_level >= 1:
            profanity.load_censor_words()

    @staticmethod
    def censor_on(string):
        return profanity.censor(string)

    @staticmethod
    def censor_off(string):
        return string

    def censor(self, string):
        if self.censor_level == 0:
            return self.censor_off(string)
        else:
            return self.censor_on(string)

