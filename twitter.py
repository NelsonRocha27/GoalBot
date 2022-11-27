import tweepy
from dotenv import load_dotenv
import os


# override tweepy.StreamListener to add logic to on_status
class StreamListener(tweepy.Stream):
    twitter = None

    def Set_Twitter(self, twitter):
        self.twitter = twitter

    def on_status(self, status):
        if status.author.id not in self.twitter.author_id:
            return
        print(status)
        self.twitter.Set_Current_Tweet(status)
        self.twitter.Set_Full_Text()
        if self.twitter.Check_If_Contains_Video():
            if self.twitter.Look_For_Keywords_In_Tweet():
                self.twitter.new_tweet = True
                pass
        else:
            pass


class Twitter:
    auth = None
    api = None
    consumer_key = None
    consumer_secret = None
    access_token = None
    access_token_secret = None
    bearer_token = None
    screen_names = None
    last_tweet_time = None
    author_id = None
    current_tweet = None
    list_of_keywords = None
    guild_id = None
    new_tweet = False
    text_channel_id = None
    link = None
    full_text = None

    def __init__(self, screen_names):
        load_dotenv()

        self.Init_Class_Variables()

        self.consumer_key = os.getenv('CONSUMERKEY')
        self.consumer_secret = os.getenv('CONSUMERSECRET')
        self.access_token = os.getenv('ACCESSTOKEN')
        self.access_token_secret = os.getenv('ACCESSTOKENSECRET')
        self.bearer_token = os.getenv('BEARERTOKEN')
        self.auth = tweepy.AppAuthHandler(self.consumer_key,
                                          self.consumer_secret)
        self.api = tweepy.API(self.auth)
        self.Set_Twitter_Account(screen_names)

    def Init_Class_Variables(self):
        self.auth = None
        self.api = None
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_token_secret = None
        self.bearer_token = None
        self.screen_names = []
        self.last_tweet_time = None
        self.author_id = []
        self.current_tweet = None
        self.list_of_keywords = []
        self.guild_id = None
        self.new_tweet = False
        self.text_channel_id = None
        self.link = None

    def Set_Twitter_Account(self, screen_names):
        self.screen_names = screen_names
        self.Get_Last_Tweet_Info()
        self.Set_Listener()

    def Get_Last_Tweet_Info(self):
        for screen_name in self.screen_names:
            for tweet in self.api.user_timeline(screen_name=screen_name, tweet_mode='extended', count=1):
                self.author_id.append(tweet.author.id)
                if self.last_tweet_time is None or tweet.created_at > self.last_tweet_time:
                    self.last_tweet_time = tweet.created_at

    def Set_Guild_Id(self, guild_id):
        self.guild_id = guild_id

    def Get_Guild_Id(self):
        return self.guild_id

    def Set_New_Tweet(self, val):
        self.new_tweet = val

    def Get_New_Tweet(self):
        return self.new_tweet

    def Set_Current_Tweet(self, tweet):
        self.current_tweet = tweet

    def Get_Current_Tweet(self):
        return self.current_tweet

    def Set_Text_Channel_ID(self, channel_id):
        self.text_channel_id = channel_id

    def Get_Text_Channel_ID(self):
        return self.text_channel_id

    def Set_Full_Text(self):
        self.full_text = self.current_tweet.text
        if hasattr(self.current_tweet, 'extended_tweet'):
            if 'full_text' in self.current_tweet.extended_tweet:
                print('full_text')
                self.full_text = self.current_tweet.extended_tweet.get('full_text')
                print(self.full_text)

    def Get_Full_Text(self):
        return self.full_text

    def Get_Tweet_Link(self):
        return self.link

    def Set_List_Of_Keywords(self, list_of_keywords):
        self.list_of_keywords = list_of_keywords

    def Check_If_Contains_Video(self):
        print('Checking for a video...')
        if hasattr(self.current_tweet, 'extended_tweet'):
            if 'extended_entities' in self.current_tweet.extended_tweet:
                if 'expanded_url' in self.current_tweet.extended_tweet['extended_entities']['media'][0]:
                    if self.current_tweet.created_at > self.last_tweet_time:
                        self.last_tweet_time = self.current_tweet.created_at
                        self.link = self.current_tweet.extended_tweet['extended_entities']['media'][0].get(
                            'expanded_url')
                        if "/video/" in self.link:
                            print(self.link)
                            return True
                        else:
                            print('There is not a video link {0}.'.format(self.link))
                    else:
                        print('This tweet is older.')
                else:
                    print('There is no video in tweet {0}.'.format(self.current_tweet))
            else:
                print('There are no extended entities in tweet {0}.'.format(self.current_tweet))
        elif hasattr(self.current_tweet, 'extended_entities'):
            if 'expanded_url' in self.current_tweet.extended_entities['media'][0]:
                if self.current_tweet.created_at > self.last_tweet_time:
                    self.last_tweet_time = self.current_tweet.created_at
                    self.link = self.current_tweet.extended_entities['media'][0].get('expanded_url')
                    if "/video/" in self.link:
                        print(self.link)
                        return True
                    else:
                        print('There is not a video link {0}.'.format(self.link))
                else:
                    print('This tweet is older.')
            else:
                print('There is no video in tweet {0}.'.format(self.current_tweet))
        else:
            print('There is no extended tweet or extended entities in tweet {0}.'.format(self.current_tweet))

        return False

    def Look_For_Keywords_In_Tweet(self):
        if self.list_of_keywords is not None:
            for keyword in self.list_of_keywords:
                print(keyword)
                print(self.full_text)
                if keyword in self.Get_Full_Text():
                    return True
        else:
            print('No list of keywords provided.')

        print('This tweet has no wanted keywords.')
        return False

    def Set_Listener(self):
        tweetStream = StreamListener(consumer_key=self.consumer_key,
                                     consumer_secret=self.consumer_secret,
                                     access_token=self.access_token,
                                     access_token_secret=self.access_token_secret)

        tweetStream.Set_Twitter(self)
        try:
            tweetStream.filter(follow=self.author_id, threaded=True)
            tweetStream.sample(threaded=True)
        except Exception:
            pass
