import subprocess

def send_notification(title, message):
    applescript_command = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", applescript_command])
