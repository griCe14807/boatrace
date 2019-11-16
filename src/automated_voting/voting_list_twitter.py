import twitter

auth = twitter.OAuth(consumer_key="",
consumer_secret="",
token="",
token_secret="")

t = twitter.Twitter(auth=auth)

#ツイートのみ
status="Hello,World" #投稿するツイート
t.statuses.update(status=status) #Twitterに投稿