import requests
import json

idMals = []
idAnilists = []

# fetches data from the txt file where you have the anime you want to track as MAL or AniList links
with open("/Users/shinismac98/Library/Mobile Documents/com~apple~CloudDocs/anime_to_track.txt", "r+") as anime_tracker:
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

url = 'https://graphql.anilist.co' # queries call to this link


# Fetch data from MAL links
combined_data_mal = []

for idMal in idMals:
    variables = {'idMal': idMal}
    # Make the HTTP Api request
    response = requests.post(url, json={'query': ANIME_QUERY, 'variables': variables})
    data_readable = json.loads(response.text)
    anime_name = data_readable['data']['Media']['title']['romaji']
    anime_status = data_readable['data']['Media']['status']
    anime_year = data_readable['data']['Media']['seasonYear']
    anime_enddate = data_readable['data']['Media']['endDate']
    mal_tracked = (anime_name, anime_status, anime_year, anime_enddate)
    combined_data_mal.append(mal_tracked)

# Fetch data from AniList links
combined_data_anilist = []

for idAnilist in idAnilists:
    variables = {'id': idAnilist}
    # Make the HTTP Api request
    response = requests.post(url, json={'query': ANIME_QUERY, 'variables': variables})
    data_readable = json.loads(response.text)
    anime_name = data_readable['data']['Media']['title']['romaji']
    anime_status = data_readable['data']['Media']['status']
    anime_year = data_readable['data']['Media']['seasonYear']
    anime_enddate = data_readable['data']['Media']['endDate']
    anilist_tracked = (anime_name, anime_status, anime_year, anime_enddate)
    combined_data_anilist.append(anilist_tracked)

combined_data = combined_data_anilist + combined_data_mal

with open("anime_data.txt", "w") as file_temp:
    # https://docs.python.org/3/library/json.html
    # data_readable and json.dump are used because response.text by default returns utf-8 characters as strings that look like this: \u2019
    json.dump(combined_data, file_temp, ensure_ascii=False, indent=4)
    # tuples in python, mal_tracked and anilist_tracked, are converted to arrays in json.

# def fetch_status(variables):
#   response = requests.post(url, json={'query': ANIME_QUERY, 'variables': variables})
#   data_readable = json.loads(response.text)
#   anime_data = {
#     'anime_name' : data_readable['data']['Media']['title']['romaji'],
#     'anime_status' : data_readable['data']['Media']['status'],
#     'anime_year' : data_readable['data']['Media']['seasonYear'],
#     'anime_enddate' : data_readable['data']['Media']['endDate']
#   }
#   return anime_data

# if 
