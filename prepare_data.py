import requests
import json
from time import sleep

idMals = []
idAnilists = []
animefile_path = "/Users/shinismac98/Library/Mobile Documents/com~apple~CloudDocs/anime_to_track.txt"
anialert_path = "/Users/shinismac98/Documents/GitHub/AniAlert/"

# fetches data from the txt file where you have the anime you want to track as MAL or AniList links
with open(animefile_path, "r+") as anime_tracker:
    for anime in anime_tracker:
        if 'myanimelist' in anime:
            link_separated = anime.rstrip().split('/')
            mal_id = int(link_separated[4])
            idMals.append(mal_id)
        elif 'anilist' in anime:
            link_separated = anime.rstrip().split('/')
            anilist_id = int(link_separated[4])
            idAnilists.append(anilist_id)

# Here we define our query as a multi-line string
ANIME_QUERY = '''
query ($id: Int, $idMal: Int) { # Define which variables will be used in the query (id)
  Media (id: $id, idMal: $idMal, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
    id
    idMal
    title {
      romaji
      english
      native
    }
    status
    season
    seasonYear
    endDate {
        year
        month
        day
    }
  }
}
'''

def fetch_data(variables):
  url = 'https://graphql.anilist.co' # query calls to this link
  try:
    response = requests.post(url, json={'query': ANIME_QUERY, 'variables': variables})
    data_readable = response.json()
    anime_data = {
      'anime_id' : data_readable['data']['Media']['id'],
      'anime_name' : data_readable['data']['Media']['title']['romaji'],
      'anime_status' : data_readable['data']['Media']['status'],
      'anime_year' : data_readable['data']['Media']['seasonYear'],
      'anime_enddate' : data_readable['data']['Media']['endDate']
    }
    return anime_data
  except requests.RequestException as e:
    print(f"There was an error: {e}")
    return None

# Fetch data from MAL links
combined_data = []

for idMal in idMals:
    query_variable = {'idMal': idMal}
    combined_data.append(fetch_data(query_variable))

for idAnilist in idAnilists:
    query_variable = {'id': idAnilist}
    combined_data.append(fetch_data(query_variable))

with open(f"{anialert_path}/anime_data.txt", "w") as file_temp:
    # https://docs.python.org/3/library/json.html
    # data_readable and json.dump are used because response.text by default returns utf-8 characters as strings that look like this: \u2019
    json.dump(combined_data, file_temp, ensure_ascii=False, indent=4)
