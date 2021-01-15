import json
import numpy
import pandas
from fuzzywuzzy import fuzz


file_path = "/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/Corpora/TwiConv/time_and_tweets.json"

with open(file_path, 'r') as file:
    tweets = json.load(file)




k = len(tweets)

similarity = numpy.empty((k, k), dtype=float)

for i, ac in enumerate(tweets.values()):
    for j, bc in enumerate(tweets.values()):
        if i > j:
            continue

        if i == j:
            sim = 100
        else:
            sim = fuzz.ratio(ac, bc)

        similarity[i, j] = sim
        similarity[j, i] = sim

data_frame_similarity = pandas.DataFrame(similarity, index=tweets, columns=tweets)
print(data_frame_similarity[0])
