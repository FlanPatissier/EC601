# encoding: utf-8
# Author - Flora Zou


import tweepy  # https://github.com/tweepy/tweepy



# set Twitter API credentials
consumer_key = 'Lr9BYDvg5Ed4qPnAvbgH5qM3x'
consumer_secret = 'M9zTp4mt52eknUJctlyZ7S6zefXbt93WV2Ox0ypfcTZn3FBtNK'
access_token = '1437467670618669058-Xc9586GVlPnkPCgRwo5wu76Yz08EIT'
access_secret = 'KulxyCEFXmXUO9KWTZaj7gB4bhyEVYMjYQkIF2I9ZLc6p'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#User_ID = '2244994945'

def print_user_tweets(user_name):
    # return the usernames and their twitters
	user_tweets = api.user_timeline(user_name, count = 5, tweet_mode = 'extended')
	for tweet in user_tweets:
		print(tweet.user.name)
		print(tweet.full_text)
		print('')

def get_trends_by_location(location_of_interest):
    #trend what is the hottsst trend in that area
	location_trends = api.trends_place(location_of_interest)
	for trend in location_trends[0]["trends"][:10]:
		print(trend["name"])


def find_followers(user_name):
	# getting the followers list
	followers = api.followers_ids(user_name)
	print(user_name + " has " + str(len(followers)) + " followers.")
	print(" ")

def get_creation_time(user_name):
	user = api.get_user(user_name)

	# fetching the create_at attribute
	created_at = user.created_at
	print("The user was created on : " + str(created_at))
	print(" ")

def get_description(user_name):
	# searching for the description
	user = api.get_user(user_name)
	description = user.description
	print("The description of the user is : " + description)
	print(" ")

def find_languages(twi_ID):
	id = 1273220141417816064
	# fetching the status
	status = api.get_status(id)
	# fetching the lang attribute
	lang = status.lang
	print("The language of the status is : " + lang)
	print(" ")

#if __name__ == "__main__":
print("User Tweet - Taylor Swift")
print_user_tweets("@taylorswift13")

print("Find_followers of Taylor Swift")
find_followers("@taylorswift13")

print("Descriptions of Taylor Swift")
get_description("@taylorswift13")

print("Get the creation time of the CNN")
get_creation_time("@cnnbrk")

print("Location Trending - Los Angeles Test")
get_trends_by_location(2442047)

print("Finding the language of a certain twi")
find_languages(1273220141417816064)



