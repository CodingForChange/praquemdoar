from TwitterAPI import TwitterAPI
from config import TWITTER_API_KEY, TWITTER_API_SECRET
from config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET

api = TwitterAPI(TWITTER_API_KEY, TWITTER_API_SECRET,
                 TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)

request = api.request('statuses/filter', {'track': 'praquemdoar'})

for tweet in request.get_iterator():
    print tweet
