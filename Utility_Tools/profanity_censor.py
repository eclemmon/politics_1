from better_profanity import profanity


class Censor:
    """
    Censor class to censor a string so that trolls can't do their thing.
    """
    def __init__(self, censor_level: int = 0):
        """
        Initialization for Censor
        :param censor_level: int
        """
        self.censor_level = censor_level
        if self.censor_level >= 1:
            profanity.load_censor_words()

    @staticmethod
    def censor_on(string):
        """
        Censors the given string.
        :param string: str
        :return: str
        """
        return profanity.censor(string)

    def censor(self, string):
        """
        General function that either censors a string or doesn't based on this input censor_level
        :param string: str
        :return: str
        """
        if self.censor_level == 0:
            return string
        else:
            return self.censor_on(string)

