from flask import Flask, render_template, request, redirect, url_for
# from app import app
app = Flask(__name__)
import requests
import json
from forms import SearchPlaylist
from config import Config
app.config.from_object(Config)
from urllib.parse import quote
'''
TO DO:
- Get bearer token dynamically for each user
- Cut playlist identifier out of URL entered in searchBar input
'''

#AUTH GUIDE: https://github.com/drshrey/spotify-flask-auth-example/blob/master/main.py

base_url = 'https://api.spotify.com/v1/'
# get bearer token dynamically somehow
# headers = {'Authorization': "Bearer BQDQ_3MtGynPPeUImxIHR5UjXXqAsK5wLIFi76LPhUU341Crv3Fqj2-YpqoDOB7wKQO2qdi6WREHXk_SMTWBK5JATuIl4GdcWbUga7wTEbA08LZbSh8-2Vc71GCwYBmkheKZ8_QJNA6K9vUuRw"}

CLIENT_ID = 'ec23aaee493741eba1126b2803ab7ef8'
CLIENT_SECRET = '133e431e70964c968d5ace30e3ef2608'

BASE_64 = 'ZWMyM2FhZWU0OTM3NDFlYmExMTI2YjI4MDNhYjdlZjg6MTMzZTQzMWU3MDk2NGM5NjhkNWFjZTMwZTNlZjI2MDg='

AUTH_ENDPOINT = 'https://accounts.spotify.com/api/token'
GRANT_TYPE = 'CLIENT_CREDENTIALS'
headers = {'Authorization': 'Basic ZWMyM2FhZWU0OTM3NDFlYmExMTI2YjI4MDNhYjdlZjg6MTMzZTQzMWU3MDk2NGM5NjhkNWFjZTMwZTNlZjI2MDg='}
payload = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
BASE64_ID = 'ZWMyM2FhZWU0OTM3NDFlYmExMTI2YjI4MDNhYjdlZjg='
BASE64_SECRET = 'MTMzZTQzMWU3MDk2NGM5NjhkNWFjZTMwZTNlZjI2MDg='
token = requests.post(AUTH_ENDPOINT, data={'grant_type':'client_credentials'}, headers=headers)
print(token)
print(token.json())
tjson = token.json() 
print(tjson['access_token'])

headers = {'Authorization': "Bearer " + tjson['access_token']}

@app.route('/', methods=['GET', 'POST'])
def index():
    
    playlist_url = ""
    playlist_id = ""
    result = []
    searchBar = SearchPlaylist(prefix="searchBar")
    if searchBar.validate_on_submit() and searchBar.submit.data:
        # store input data in playlist_url variable
        playlist_url = searchBar.playlist_url.data
        playlist_id = playlist_url[-22:]
        # the playlist ID should be 22 chars long
        # suffix after ID is 26 chars long
        print(playlist_id)
        # results(playlist_url)
        # https://open.spotify.com/user/1234702250/playlist/5DMVuXqC5Efdx1h4WH7veM?si=9lt-ge6kQZa8mRdJlJQqHA
        # result = results(playlist_id)
        # print(results)
        print(results(playlist_id))
        result = results(playlist_id)
        print(result[0])
    
    return render_template('search.html', searchBar=searchBar, playlist_id=playlist_id, result=result)


def results(playlist_id):
    print(playlist_id)
    tracks_url = base_url + 'playlists/' + playlist_id + '/tracks'
    url_fields = '?fields=items(added_by.id%2C%20track(name,artists,id))'
    limit = '&limit=2'
    url = tracks_url + url_fields + limit
    print(url)
    response = requests.get(url, headers=headers)
    tracks_data = response.json() 
    print(tracks_data)
    playlist_data = []
    # print(tracks_data)
    for track in tracks_data['items']:
        track_title = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        track_id = track['track']['id']

        # get audio features for each track
        audio_features_url = 'https://api.spotify.com/v1/audio-features/' + track_id
        response = requests.get(audio_features_url, headers=headers)
        features = response.json() 
        
        dance_rating = features['danceability']
        energy = features['energy']
        valence = features['valence']
        bpm = features['tempo']
        signature = features['time_signature']
        acousticness = features['acousticness']
        key = features['key']
        instrumentalness = features['instrumentalness']
        liveness = features['liveness']
        loudness = features['loudness']
        speechiness = features['speechiness']
        track_href = features['track_href']
        analysis_url = features['analysis_url']

        playlist_data.append({
            "track_title": track_title,
            "artist_name": artist_name,
            "track_id": track_id,
            "dance_rating": dance_rating,
            "energy": energy,
            "valence": valence,
            "bpm": bpm,
            "signature": signature,
            "acouticness": acousticness,
            "key": key,
            "instrumentalness": instrumentalness,
            "liveness": liveness,
            "loudness": loudness,
            "speechiness": speechiness,
            "track_href": track_href,
            "analysis_url": analysis_url
        })

    return playlist_data

if __name__ == '__main__':
    app.run(debug = True)
