'''
This program handles the notification part.
It reads the finished_airing.txt file, a list of anime that have finished airing.
'''
import subprocess
import json
from datetime import datetime

APP_NAME = "AniAlert"

# Use subprocess to trigger an Applescript automation script called "osascript"
def send_notification(title, message):
    applescript_command = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", applescript_command])

with open('anime_data.txt', 'r+') as old_data:
    anime_info = json.load(old_data)

with open('finished_airing.txt', 'w') as finished_anime:
    for title in anime_info:
        anime_name = title[0]
        anime_status = title[1]
        anime_year = title[2]
        anime_end_year = title[3]['year']
        anime_end_month = title[3]['month']
        anime_end_day = title[3]['day']
        if anime_status == 'FINISHED':
            date_number = str(anime_end_year).zfill(4) + str(anime_end_month).zfill(2) + str(anime_end_day).zfill(2)
            end_date = datetime.strptime(date_number, '%Y%m%d').strftime('%d %B, %Y (%A)')
            finished_anime.write(f'{anime_name}' + '\n')

# Read the anime's name from the txt file for the notification_message
with open("finished_airing.txt", "r+") as anime_file:
    for anime in anime_file:
        notification_message = f"{anime.rstrip()} has finished airing on {end_date}"
        send_notification(title=APP_NAME, message=notification_message)
    
    # once the notification has been sent, let us refresh the file
    anime_file.seek(0)
    anime_file.truncate()
