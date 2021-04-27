import requests
import matplotlib.pyplot as plt
import numpy as np

API_KEY = '1af0326d8ca0e6dfb7987ac327434d90'
API_SECRET = '835d2af420c842d5180aace5c0a5fc44'

url = 'http://ws.audioscrobbler.com/2.0/'

username = "seandiacono"
lastfm_password_hash = 'a1d7e3b4e78bcfab55dd18c009fa2b37'


class Artist():

    def __init__(self, name, image_url):
        self.name = name
        self.image_url = image_url
        self.playcount = []

    def set_playcount(self, playcount):
        self.playcount = playcount


top_artist_params = {
    'method': 'user.getTopArtists',
    'format': 'json',
    'user': username,
    'period': 'overall',
    'limit': 10,
    'api_key': API_KEY
}

r = requests.get('https://ws.audioscrobbler.com/2.0/',
                 params=top_artist_params)

result = r.json()

top_artists = []

for artist in result["topartists"]["artist"]:
    name = artist["name"]
    url = artist["image"][2]["#text"]
    temp = Artist(name=name, image_url=url)
    top_artists.append(temp)


# years = [('1514764800', '1546261199'), ('1546300809', '1577797139'),
    #  ('1577836800', '1609419599'), ('1609459200', '1640955599')]

years = [('1514764800', '1546261199'), ('1546300809', '1577797139'),
         ('1577836800', '1609419599')]

for year in years:
    print("Getting Year")
    params = {
        'method': 'user.getWeeklyArtistChart',
        'format': 'json',
        'user': username,
        'from': year[0],
        'to': year[1],
        'api_key': API_KEY
    }

    r = requests.get('https://ws.audioscrobbler.com/2.0/',
                     params=params)

    result = r.json()

    for artist in top_artists:
        found = False
        for x in result["weeklyartistchart"]["artist"]:
            if x["name"] == artist.name:
                artist.playcount.append(int(x["playcount"]))
                found = True
        if not found:
            artist.playcount.append(0)

dates = [2018, 2019, 2020]

fig, ax = plt.subplots()
for artist in top_artists:
    ax.plot(dates, artist.playcount, label=artist.name)

plt.legend()
plt.show()
