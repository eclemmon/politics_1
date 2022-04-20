from typing import Union

class SentimentDict:
    """
    SentimentDict class. A wrapper for the dictionary class with some extra logic to shorthand operations on sentiment
    dictionaries from nltk's VADER
    """
    def __init__(self, sent: Union[None, dict] = None, x_averaged: Union[None, int] = None):
        """
        Initialization for SentimentDict
        :param sent: dict
        :param x_averaged: int, number of times averaged
        """
        if sent is None:
            self.sent_dict = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
        else:
            self.sent_dict = sent

        if x_averaged is None:
            self.x_averaged = 1
        else:
            self.x_averaged = x_averaged

    def __add__(self, other):
        """
        Class override for addition between two SentimentDicts
        :param other: SentimentDict
        :return: SentimentDict
        """
        if isinstance(other, SentimentDict):
            res = {}
            for k in self.sent_dict.keys():
                res[k] = self.sent_dict[k] + other.sent_dict[k]
            return SentimentDict(res)
        else:
            return NotImplemented

    def __sub__(self, other):
        """
        Class override for subtraction between two SentimentDicts
        :param other: SentimentDict
        :return: SentimentDict
        """
        if isinstance(other, SentimentDict):
            res = {}
            for k in self.sent_dict.keys():
                res[k] = self.sent_dict[k] - other.sent_dict[k]
            return SentimentDict(res)
        else:
            return NotImplemented

    def average(self, other):
        """
        Gets the mean average of two dictionaries. WARNING: does not update the x_averaged value. Use add_value_average
        in that case.
        :param other: SentimentDict
        :return: SentimentDict
        """
        if isinstance(other, SentimentDict):
            res = {}
            for k in self.sent_dict.keys():
                res[k] = (self.sent_dict[k] + other.sent_dict[k]) / 2
            return SentimentDict(res)
        else:
            return NotImplemented

    def add_value_average(self, other):
        """
        Gets the mean average of two dictionaries while tracking the overall number of times the returned dictionary
        has been averaged. This allows for proper weighting of the meaned values, while allowing other SentimenDicts
        to be garbage collected
        :param other: SentimentDict
        :return: SentimentDict
        """
        if isinstance(other, SentimentDict):
            res = {}
            for k in self.sent_dict.keys():
                res[k] = self.sent_dict[k] + ((other.sent_dict[k] - self.sent_dict[k]) / (self.x_averaged + 1))
            return SentimentDict(res, self.x_averaged + 1)
        else:
            return NotImplemented

    def abs_difference(self, other):
        """
        Get the absolute value of the difference between the values of two SentimentDicts
        :param other: SentimentDict
        :return: SentimentDict
        """
        if isinstance(other, SentimentDict):
            res = {}
            for k in self.sent_dict.keys():
                res[k] = abs(self.sent_dict[k] - other.sent_dict[k])
            return SentimentDict(res)
        else:
            return NotImplemented

    def __repr__(self):
        """
        Class override for SentimentDict representation
        :return: str
        """
        return '<{0}.{1} object at {2} || {3}>'.format(
            type(self).__module__, type(self).__qualname__, hex(id(self)), self.__str__())

    def __str__(self):
        """
        Class override for str(SentimentDict).
        :return: str
        """
        return self.sent_dict


if __name__ == '__main__':
    avg_sent = SentimentDict()
    avg_sent = avg_sent + SentimentDict({'neg': 0.45, 'neu': 0.84, 'pos': 0.2, 'compound': 0.846})
    avg_sent = avg_sent + SentimentDict({'neg': 0.45, 'neu': 0.84, 'pos': 0.2, 'compound': 0.846})
    avg_sent = avg_sent.average(SentimentDict())
    print(avg_sent)
    avg_sent = avg_sent.add_value_average(SentimentDict({'neg': 1, 'neu': 1, 'pos': 1, 'compound': 1}))
    print(avg_sent)
    avg_sent = avg_sent.add_value_average(SentimentDict())
    print(avg_sent)

