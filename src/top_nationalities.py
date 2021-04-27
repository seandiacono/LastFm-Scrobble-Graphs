import requests
import matplotlib.pyplot as plt
import numpy as np
import musicbrainzngs as brainz
from collections import Counter

API_KEY = '1af0326d8ca0e6dfb7987ac327434d90'
API_SECRET = '835d2af420c842d5180aace5c0a5fc44'

url = 'http://ws.audioscrobbler.com/2.0/'

username = "seandiacono"
lastfm_password_hash = 'a1d7e3b4e78bcfab55dd18c009fa2b37'

brainz.set_useragent(app="nationalities", version=1)


class Artist():

    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.playcount = []

    def set_playcount(self, playcount):
        self.playcount = playcount


top_artist_params = {
    'method': 'user.getTopArtists',
    'format': 'json',
    'user': username,
    'period': 'overall',
    'limit': 50,
    'api_key': API_KEY
}

r = requests.get('https://ws.audioscrobbler.com/2.0/',
                 params=top_artist_params)

result = r.json()

nationalities = []
for artist in result["topartists"]["artist"]:
    id = artist["mbid"]
    name = artist["name"]
    result = brainz.search_artists(name)
    result = result["artist-list"][0]
    # print(result)
    try:
        nationality = result["country"]
    except:
        print("Country for " +
              artist["name"] + " not found. Enter manually: ")
        nationality = input()
    nationalities.append(nationality)

nation_dict = Counter(nationalities)

plt.pie(nation_dict.values(), labels=nation_dict.keys())
plt.show()
