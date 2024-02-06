'''
This program handles the notification part.
It reads the finished_airing.txt file, a list of anime that have finished airing.
'''
import subprocess
import json
from datetime import datetime
from prepare_data import fetch_data
import logging

log_file_path = "/Users/shinismac98/Documents/AniAlertlog.txt"
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("AniAlert script started")

APP_NAME = "AniAlert"

# Use subprocess to trigger an Applescript automation script called "osascript"
def send_notification(title, message):
    try:
        applescript_command = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", applescript_command])
        logging.info(f"Notification sent for {title}")
    except Exception as e:
        logging.error(f"Failed to send notification for {title}: {e}")

def status_change(anime_details):
    old_status = anime_details['anime_status']
    anime_query_variable = {'id': anime_details['anime_id']}
    current_data = fetch_data(anime_query_variable)
    current_status = current_data['anime_status']
    if old_status != 'FINISHED':
        if current_status != old_status:
            return True
        else:
            return False

try:
    with open('anime_data.txt', 'r+') as old_data:
        anime_info = json.load(old_data)

    with open('finished_airing.txt', 'w') as finished_anime:
        for title in anime_info:
            anime_end_year = title['anime_enddate']['year']
            anime_end_month = title['anime_enddate']['month']
            anime_end_day = title['anime_enddate']['day']
            anime_name = title['anime_name']
            if status_change(title):
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

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    logging.info("AniAlert script completed.")
