class SentimentDict:
    def __init__(self, sent=None, x_averaged=None):
        if sent is None:
            self.sent_dict = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
        else:
            self.sent_dict = sent

        if x_averaged is None:
            self.x_averaged = 1
        else:
            self.x_averaged = x_averaged

    def __add__(self, other):
        res = {}
        for k in self.sent_dict.keys():
            res[k] = self.sent_dict[k] + other.sent_dict[k]
        return SentimentDict(res)

    def __sub__(self, other):
        res = {}
        for k in self.sent_dict.keys():
            res[k] = self.sent_dict[k] - other.sent_dict[k]
        return SentimentDict(res)

    def average(self, other):
        res = {}
        for k in self.sent_dict.keys():
            res[k] = (self.sent_dict[k] + other.sent_dict[k]) / 2
        return SentimentDict(res)

    def add_value_average(self, other):
        res = {}
        for k in self.sent_dict.keys():
            res[k] = self.sent_dict[k] + ((other.sent_dict[k] - self.sent_dict[k]) / (self.x_averaged + 1))
        return SentimentDict(res, self.x_averaged + 1)

    def abs_difference(self, other):
        res = {}
        for k in self.sent_dict.keys():
            res[k] = abs(self.sent_dict[k] - other.sent_dict[k])
        return SentimentDict(res)

    def __repr__(self):
        return self

    def __str__(self):
        return str(self.sent_dict)


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

