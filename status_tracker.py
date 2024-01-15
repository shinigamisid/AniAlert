import requests
import json

idMals = []
ids = []

with open("/Users/shinismac98/Library/Mobile Documents/com~apple~CloudDocs/anime_to_track.txt", "r+") as anime_tracker:
    for anime in anime_tracker:
        if 'myanimelist' in anime:
            link_separated = anime.rstrip().split('/')
            mal_id = int(link_separated[4])
            idMals.append(mal_id)
        elif 'anilist' in anime:
            link_separated = anime.rstrip().split('/')
            anilist_id = int(link_separated[4])
            ids.append(anilist_id)

# Here we define our query as a multi-line string
query = '''
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
  }
}
'''

url = 'https://graphql.anilist.co'

# Define our query variables and values that will be used in the query request

combined_data_mal = []

for idMal in idMals:
    variables = {'idMal': idMal}
    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    data_readable = json.loads(response.text)
    anime_name = data_readable['data']['Media']['title']['romaji']
    anime_status = data_readable['data']['Media']['status']
    mal_tracked = (anime_name, anime_status)
    combined_data_mal.append(mal_tracked)

combined_data_anilist = []

for id in ids:
    variables = {'id': id}
    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    data_readable = json.loads(response.text)
    anime_name = data_readable['data']['Media']['title']['romaji']
    anime_status = data_readable['data']['Media']['status']
    anilist_tracked = (anime_name, anime_status)
    combined_data_anilist.append(anilist_tracked)

combined_data = combined_data_anilist + combined_data_mal

with open("temp.txt", "w") as file_temp:
    # https://docs.python.org/3/library/json.html
    # data_readable and json.dump are used because response.text by default returns utf-8 characters as strings that look like this: \u2019
    json.dump(combined_data, file_temp, ensure_ascii=False, indent=4)
    # tuples in python, mal_tracked and anilist_tracked, are converted to arrays in json.
