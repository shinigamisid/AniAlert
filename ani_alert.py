from notification import send_notification

APP_NAME = "AniAlert"

# read the anime's name from the txt file for the notification_message
anime_list = []
anime_file = open("finished_airing.txt", 'r')

for anime in anime_file:
    notification_message = f"{anime.rstrip()} has finished airing"
    send_notification(title=APP_NAME, message=notification_message)

# once the notification has been sent, let us remove the anime's name
