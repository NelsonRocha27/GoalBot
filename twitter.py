import tweepy


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.Stream):
    user_id = None

    def Set_User_ID(self, user_id):
        self.user_id = user_id

    def on_status(self, status):
        if status.author.id != self.user_id:
            return
        print(status)


class Twitter:
    auth = None
    api = None
    client = None
    consumer_key = None
    consumer_secret = None
    access_token = None
    access_token_secret = None
    bearer_token = None

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, bearer_token):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.bearer_token = bearer_token
        self.auth = tweepy.AppAuthHandler(self.consumer_key,
                                          self.consumer_secret)
        self.api = tweepy.API(self.auth)
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret)

        # for status in self.lol.get_users_tweets(40019154):
        #   print(status)
        for tweet in self.api.user_timeline(screen_name='Reuters', tweet_mode='extended', count=1):
            if hasattr(tweet, "extended_entities"):
                if 'media' in tweet.extended_entities:
                    if 'video_info' in tweet.extended_entities['media'][0]:
                        self.last_tweet = tweet.created_at


class TwitterAccount(Twitter):
    screen_name = None
    last_tweet_time = None
    author_id = None
    current_tweet = None

    def __init__(self, screen_name):
        self.screen_name = screen_name
        self.Get_Last_Tweet_Info(self)

    def Get_Last_Tweet_Info(self):
        for tweet in self.api.user_timeline(screen_name=self.screen_name, tweet_mode='extended', count=1):
            self.author_id = tweet.author.id
            self.last_tweet_time = tweet.created_at
            # if hasattr(tweet, "extended_entities"):
            #   if 'media' in tweet.extended_entities:
            #      if 'video_info' in tweet.extended_entities['media'][0]:
            #         self.last_tweet_time = tweet.created_at

    def Set_Listener(self):
        myStream = MyStreamListener(consumer_key=self.consumer_key,
                                    consumer_secret=self.consumer_secret,
                                    access_token=self.access_token,
                                    access_token_secret=self.access_token_secret)

        myStream.Set_User_ID(self.author_id)
        myStream.filter(follow=[self.author_id])
        myStream.sample(threaded=True)
