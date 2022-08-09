import os
import time

from musics import *

ID = ''
MUSICS = Musics()
MUSICS_LIST = MUSICS.getMusics()
USER = os.getenv('USER')
APIKEY = os.getenv('API_KEY')
API_ID = os.getenv('API_ID')

SPOTIFY_CODE = os.getenv('S_CODE')
REDIRECT_URL = os.getenv('REDIRECT')
ACCESS_TOKEN = ''


def get_code():
    get_code_parameter = {
        'client_id': API_ID,
        'redirect_uri': REDIRECT_URL,
        'response_type': 'code',
        'scope': "playlist-modify-public",
    }

    get_code_url = 'https://accounts.spotify.com/authorize'
    code_finder = get(url=get_code_url, params=get_code_parameter, ).url
    print(f'Follow the Url Below and To Get Your Code \n{code_finder}')


def get_access_token():
    global ACCESS_TOKEN
    code = input('Kindly Enter The Generated Code :')
    token_url = 'https://accounts.spotify.com/api/token'
    token_header = {
        'Authorization': f'Basic {SPOTIFY_CODE}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    token_parameter = {
        'grant_type': "authorization_code",
        'code': code,
        'redirect_uri': REDIRECT_URL,
    }
    ACCESS_TOKEN = post(url=token_url, params=token_parameter, headers=token_header).json()['access_token']
    print(f'YOUR ACCESS_TOKEN IS :{ACCESS_TOKEN}')


def create_playlist():
    global ACCESS_TOKEN, ID
    playlist_url = f'https://api.spotify.com/v1/users/{USER}/playlists'
    name = input('Enter Your Playlist Name :')
    description = input('Description :')

    PLAYLIST_HEADER = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }
    playlist_parameter = {
        'name': name,
        'description': description,
        'public': True
    }
    new_playlist = post(url=playlist_url, headers=PLAYLIST_HEADER, json=playlist_parameter)
    new_playlist.raise_for_status()
    ID = new_playlist.json()['id']


def search_music(music):
    PLAYLIST_HEADER = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }
    search = 'https://api.spotify.com/v1/search'
    para = {
        'q': f'{music} ,genres: ["afropop", "ghanaian hip hop", "nigerian pop"]',
        'type': ['track']
    }

    let = get(url=search, params=para, headers=PLAYLIST_HEADER)
    let.raise_for_status()
    data = let.json()['tracks']['items'][0]['uri']

    return data


def add_music_to_playlist(music):
    PLAYLIST_HEADER = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }
    global ID
    uris = search_music(music)
    add_url = f'https://api.spotify.com/v1/playlists/{ID}/tracks'
    add_music_parameter = {
        "uris": [
            uris
        ], }
    done = post(url=add_url, json=add_music_parameter, headers=PLAYLIST_HEADER)
    done.raise_for_status()


get_code()
get_access_token()
create_playlist()
for i in MUSICS_LIST:
    time.sleep(1)
    print(i)
    if len(i) > 20:
        i = i[:21]
    add_music_to_playlist(i)
