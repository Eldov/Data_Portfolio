########### Imports ############
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import base64

############ The get_app_access_token() function ############
# Description: using this function to get the authentification token from Spotify API.
def get_app_access_token(client_id, client_secret):

    auth_credentials_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_credentials_string.encode('ascii')
    auth_base64 = base64.b64encode(auth_bytes)
    auth_str = auth_base64.decode('ascii')
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_headers = {
    'Authorization': f"Basic {auth_str}",
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    auth_params = {
    'grant_type': 'client_credentials'
    }
    auth_response = requests.post(
    url=auth_url,
    data=auth_params,
    headers=auth_headers
    )
    access_token = auth_response.json()['access_token']
    bearer_token_headers = {
    'Authorization': f"Bearer {access_token}"
    }

    return bearer_token_headers

############ The get_category_playlists() function ############
# Description: contains the playlists found under category_id "latin"
def get_category_playlists(category_id, header):
  
  params = {
      "limit": "50", 
      "offset": "0"
  }   
  
  url = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists"

  playlists = requests.get(url=url, params=params, headers=header).json()
  
  temp_dict = {'description':[],
               'name':[],
               'id': [],
               'tracks_url': [],
               'total_tracks': [],
               'snapshot_id': []
              }
  # This loop will iterate through every number inside the limit.
  # Pagination should be added here for cases where the category returns more than 50 items.
  # The category "latin" is not this case.
  # I will try to add something in case the user needs categories with more playlists.
  for num in range(int(params['limit'])):
      items = list(playlists['playlists']['items'])
      
      temp_dict['description'].append(items[num]['description'])
      temp_dict['name'].append(items[num]['name'])
      temp_dict['id'].append(items[num]['id'])
      temp_dict['tracks_url'].append(items[num]['tracks']['href'])
      temp_dict['total_tracks'].append(items[num]['tracks']['total'])
      temp_dict['snapshot_id'].append(items[num]['snapshot_id'])

  # Dropping duplicates on id (playlist_id). Sometimes the API would return the same playlists twice:
  df = pd.DataFrame(data=temp_dict).drop_duplicates(subset=['id'], ignore_index = True)
  print("DataFrame 'category_playlists' created!")
  return df

############ The request_page() function ############
# Description: will be used to loop through the pages of the tracks API
def request_page(id, page, header):
    url = f"https://api.spotify.com/v1/playlists/{id}/tracks?offset={page*100}&limit=100"
    request = requests.get(url=url, headers=header).json()
    return request

############ The get_playlist() function ############
# Description: unique tracks of playlists that fall into the "latin" category_id
def get_playlist(header, category_playlists):


  temp_dict = {'album_type':[],
               'id':[],
               'name': [],
               'popularity': [],
               'uri': [],
               'playlist_id': [],
               'playlist_added_at': [],
               'followers':[],
               'artist_id': [],
               'artist_name': []
              }
  # This loop will iterate every playlist_id present in the previous df
  for id in category_playlists['id']:

    total_track = int(category_playlists.loc[category_playlists['id']==id, 'total_tracks'].iloc[0])
    # total_pagenum -> is the total tracks divided by the page limit and rounded up
    # ceil() function from math lib should also work
    total_pagenum = -(-total_track//100)

    # These are the special  url and request for the follower atribute
    url_fol = f"https://api.spotify.com/v1/playlists/{id}"
    playlist_fol = requests.get(url=url_fol, headers=header).json()
    
    # This loop will iterate through pages to get the total tracks in each page
    for pagenum in range(total_pagenum):
      # playlist -> is defined from the request_page() function
      playlist = request_page(id, pagenum, header)
      items = playlist['items']
      tracknum = len(items)

      # This loop will iterate the tracks using the total tracks in each page
      for num in range(tracknum):
        track = items[num]['track']
        artists = track['artists']

        # This loop will iterate through the total or artists in a track
        for artist in range(len(artists)):

          temp_dict['album_type'].append(track['album']['album_type'])
          temp_dict['id'].append(track['id'])
          temp_dict['name'].append(track['name'])
          temp_dict['popularity'].append(track['popularity'])
          temp_dict['uri'].append(track['uri'])
          temp_dict['playlist_id'].append(id)
          temp_dict['playlist_added_at'].append(items[num]['added_at'])
          temp_dict['followers'].append(playlist_fol['followers']['total'])
          temp_dict['artist_id'].append(artists[artist]['id'])
          temp_dict['artist_name'].append(artists[artist]['name'])

  # Dropping duplicates on id (track_id), playlist_id and artist_id.
  # Making sure the same track with the same artist won't show twice in the same playlist.
  df = pd.DataFrame(data=temp_dict).drop_duplicates(subset=['id', 'playlist_id', 'artist_id'], ignore_index = True)
  print("DataFrame 'playlist' created!")
  return df

############ The category_playlists_records dataset ############
# Here I just reordered the category_playlists df and called it category_playlists_records, the first dataset.

def get_category_playlists_records(category_playlists):

    df = category_playlists[['description',
                             'name',
                             'id',
                             'tracks_url',
                             'total_tracks',
                             'snapshot_id'
                             ]]
    
    print("DataFrame 'category_playlists_records' created!")
    df.to_csv('./csv/category_playlists_records.csv.gz')
    print("File 'category_playlists_records.csv.gz' created!")
    return df

############ The playlist_records dataset ############
def get_playlist_records(playlist):
    temp_dict = {
        'id': [],
        'followers': []
    }
    temp_dict['id'] = playlist['playlist_id']
    temp_dict['followers'] = playlist['followers']

    # Dropping duplicates on id (playlist_id). We only need the playlist id showing once:
    df = pd.DataFrame(data=temp_dict).drop_duplicates(subset=['id'], ignore_index = True)
    print("DataFrame 'playlist_records' created!")
    df.to_csv('./csv/playlist_records.csv.gz')
    print("File 'playlist_records.csv.gz' created!")
    return df

############ The tracks_records dataset ############
def get_tracks_records(playlist):
    temp_dict = {
        'album_type': [],
        'id': [],
        'name': [],
        'popularity': [],
        'uri': []
    }
    temp_dict['album_type'] = playlist['album_type']
    temp_dict['id'] = playlist['id']
    temp_dict['name'] = playlist['name']
    temp_dict['popularity'] = playlist['popularity']
    temp_dict['uri'] = playlist['uri']

    # Dropping duplicates on id (track id). We only need the track id and its records showing once:
    df = pd.DataFrame(data=temp_dict).drop_duplicates(subset=['id'], ignore_index = True)
    print("DataFrame 'tracks_records' created!")
    df.to_csv('./csv/tracks_records.csv.gz')
    print("File 'tracks_records.csv.gz' created!")
    return df

############ The playlist_track_id_records dataset ############
def get_playlist_track_id_records(playlist):
    temp_dict = {
        'playlist_id': [],
        'playlist_added_at': [],
        'track_id': []
    }
    temp_dict['playlist_id'] = playlist['playlist_id']
    temp_dict['playlist_added_at'] = playlist['playlist_added_at']
    temp_dict['track_id'] = playlist['id']

    # Dropping duplicates on playlist_id and track_id. We only need the track id and playlist id showing together once:
    df = pd.DataFrame(data=temp_dict).drop_duplicates(subset=['playlist_id', 'track_id'], ignore_index = True, keep='last')
    print("DataFrame 'playlist_track_id_records' created!")
    df.to_csv('./csv/playlist_track_id_records.csv.gz')
    print("File 'playlist_track_id_records.csv.gz' created!")
    return df

############ The track_artist_id_records dataset ############
def get_track_artist_id_records(playlist):
    temp_dict = {
        'track_id': [],
        'artist_id': []
    }
    temp_dict['track_id'] = playlist['id']
    temp_dict['artist_id'] = playlist['artist_id']

    # Dropping duplicates on artist_id and track_id. We only need the artist id and the track id showing once:
    df = pd.DataFrame(data=temp_dict).drop_duplicates(subset=['artist_id', 'track_id'], ignore_index = True)
    print("DataFrame 'track_artist_id_records' created!")
    df.to_csv('./csv/track_artist_id_records.csv.gz')
    print("File 'track_artist_id_records.csv.gz' created!")
    return df

############ The artists_records dataset ############
def get_artists_records(playlist):
    temp_dict = {
        'id': [],
        'name': []
    }
    temp_dict['id'] = playlist['artist_id']
    temp_dict['name'] = playlist['artist_name']

    # Dropping duplicates on id (artist_id) and name (artist_name). We only need the artist name and its id showing once:
    df = pd.DataFrame(data=temp_dict).drop_duplicates(subset=['id', 'name'], ignore_index = True)
    print("DataFrame 'artists_records' created!")
    df.to_csv('./csv/artists_records.csv.gz')
    print("File 'artists_records.csv.gz' created!")
    return df

if __name__ == '__main__':

    ############ Loading the necessary variables ############
    load_dotenv()
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    category_id = os.environ.get("CATEGORY_ID")

    header = get_app_access_token(client_id, client_secret)

    category_playlists = get_category_playlists(category_id, header)

    playlist = get_playlist(header, category_playlists)

    category_playlists_records = get_category_playlists_records(category_playlists)

    playlist_records = get_playlist_records(playlist)

    tracks_records = get_tracks_records(playlist)

    playlist_track_id_records = get_playlist_track_id_records(playlist)

    track_artist_id_records = get_track_artist_id_records(playlist)

    artists_records = get_artists_records(playlist)
