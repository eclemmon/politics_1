import tweepy, json

# with open("twitter_credentials.json", 'r') as file:
#     credentials = json.load(file)

auth = tweepy.OAuthHandler('g6zLTugjBHXiGnweKEsqvl0o0', 'xRmlWtl4gbQAzqlT6Pu8YcN1qtYB2VJ4x5VwRaqAfsi2cE92Qm')
auth.set_access_token('1191395193615990785-Lw9IR3SK07R4AAnHq9ILwR8tkdadEz', 'iHbOPwJfLbManbKMNuWf73JjNXHHjkwBcYJLyPnwIwkWE')


api = tweepy.API(auth)

print('trying to get json tweets \n')

# status = api.user_timeline(user="1191395193615990785", count=1)[0]
# json_str = json.dumps(status._json)
# print(json_str)
print('\n', 50*'#', '\n')

print('trying to stream')

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_data(self, raw_data):
        try:
            print(raw_data)
            raw_data_as_dict = json.loads(raw_data)
            dict_reader(raw_data_as_dict)
        except:
            raise

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

def dict_reader(dict):
    for key in dict.keys():
        if type(dict[key]) == type({}):
            dict_reader(dict[key])
        else:
            print(key, ': ', dict[key])

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

stream.filter(follow=["1191395193615990785"])