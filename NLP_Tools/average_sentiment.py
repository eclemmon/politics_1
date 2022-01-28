class AverageSentiment:
    def __init__(self, sent=None, x_averaged=None):
        if sent is None:
            self.avg_sent = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
        else:
            self.avg_sent = sent

        if x_averaged is None:
            self.x_averaged = 1
        else:
            self.x_averaged = x_averaged

    def __add__(self, other):
        res = {}
        for k in self.avg_sent.keys():
            res[k] = self.avg_sent[k] + other.avg_sent[k]
        return AverageSentiment(res)

    def __sub__(self, other):
        res = {}
        for k in self.avg_sent.keys():
            res[k] = self.avg_sent[k] - other.avg_sent[k]
        return AverageSentiment(res)

    def average(self, other):
        res = {}
        for k in self.avg_sent.keys():
            res[k] = (self.avg_sent[k] + other.avg_sent[k]) / 2
        return AverageSentiment(res)

    def add_value_average(self, other):
        res = {}
        for k in self.avg_sent.keys():
            res[k] = self.avg_sent[k] + ((other.avg_sent[k] - self.avg_sent[k]) / (self.x_averaged + 1))
        return AverageSentiment(res, self.x_averaged + 1)

    def __repr__(self):
        return self

    def __str__(self):
        return str(self.avg_sent)


if __name__ == '__main__':
    avg_sent = AverageSentiment()
    avg_sent = avg_sent + AverageSentiment({'neg': 0.45, 'neu': 0.84, 'pos': 0.2, 'compound': 0.846})
    avg_sent = avg_sent + AverageSentiment({'neg': 0.45, 'neu': 0.84, 'pos': 0.2, 'compound': 0.846})
    avg_sent = avg_sent.average(AverageSentiment())
    print(avg_sent)
    avg_sent = avg_sent.add_value_average(AverageSentiment({'neg': 1, 'neu': 1, 'pos': 1, 'compound': 1}))
    print(avg_sent)
    avg_sent = avg_sent.add_value_average(AverageSentiment())
    print(avg_sent)

