'''
This program handles the notification part.
It reads the finished_airing.txt file, a list of anime that have finished airing.
'''
import subprocess

APP_NAME = "AniAlert"

# Use subprocess to trigger an Applescript automation script called "osascript"
def send_notification(title, message):
    applescript_command = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", applescript_command])

# Read the anime's name from the txt file for the notification_message
with open("finished_airing.txt", "r+") as anime_file:
    for anime in anime_file:
        notification_message = f"{anime.rstrip()} has finished airing"
        send_notification(title=APP_NAME, message=notification_message)
    
    # once the notification has been sent, let us refresh the file
    anime_file.seek(0)
    anime_file.truncate()
