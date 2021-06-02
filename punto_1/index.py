import tweepy
import json
import sys
import geocoder
from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = {'list': []}
@app.route('/', methods=['GET'])
def receive_data():
  consumer_key= "CuBrektQ6dopBRsPru2w79hBc"
  consumer_secret= "5gaqJ5UaJ4xBCCpTGJOTc7tfj3wmt5H8QVd0Ux5J0dGT9T5DMa"
  access_token= "1400136349877952514-wlgcIRPNVWuwhPfZV1izbQz572Ipyj"
  access_token_secret= "XjrpQbH7OII27pBHiEZItKtyOXGTYD8QhycaPak1sGRmK"

  # Authorization and Authentication
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)
  if __name__ == "__main__":
      # Available Locations
      available_loc = api.trends_available()
      # writing a JSON file that has the available trends around the world
      with open("available_locs_for_trend.json","w") as wp:
          wp.write(json.dumps(available_loc, indent=1))

      # Trends for Specific Country
      loc = sys.argv[0]     # location as argument variable 
      g = geocoder.osm('Colombia') # getting object that has location's latitude and longitude

      closest_loc = api.trends_closest(g.lat, g.lng)
      trends = api.trends_place(closest_loc[0]['woeid'])
      data['list'] = []
      for x in trends[0]['trends']:
        if str(x['tweet_volume']) != "None":
          print(x['name'], x['tweet_volume'])
          data['list'].append({'name': x['name'], 'tweet_volume': x['tweet_volume']})
      # writing a JSON file that has the latest trends for that location
      #with open("twitter_{}_trend.json".format(loc),"w") as wp:
        #   wp.write(json.dumps(trends, indent=1))
  return 'True'

@app.route('/dashboard')
def dashboard():
    return  data

app.run()
