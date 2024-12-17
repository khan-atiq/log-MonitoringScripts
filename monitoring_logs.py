import time
import requests
import re

# Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/xxxxxxxxxxxxxxxxxxxxxxxx"


# Function to send a Discord notification
def send_discord_notification(message):
    """Send a message to Discord via webhook."""
    payload = {
        "content": message
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("Discord notification sent successfully.")
        else:
            print(f"Failed to send Discord notification. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while sending Discord notification: {str(e)}")

# Function to tail a file line by line in real-time
def tail_file(file_path):
    """Generator to read a file line by line in real-time."""
    with open(file_path, 'r') as f:
        f.seek(0, 2)  # Move the pointer to the end of the file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)  # Sleep briefly to avoid busy-waiting
                continue
            yield line

# Function to monitor logs for a specific error
def monitor_logs(log_file):
    """Monitor the log file and alert on specific SSL error lines."""
    ssl_error_pattern = re.compile(r"SSL operation failed|OpenSSL Error", re.IGNORECASE)
    try:
        for line in tail_file(log_file):
            if ssl_error_pattern.search(line):  # Match the line with the regex
                print(f"⚠️ SSL Error Found: {line.strip()}")
                send_discord_notification(f"⚠️ SSL Error Alert on DEVELOPMENT Server : {line.strip()}")
    except FileNotFoundError:
        print(f"Log file {log_file} not found. Please check the file path.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    #log_file_path = "/opt/docker/dms/qa/dms/laravel/laravel.log"  # Replace with your log file path
    log_file_path = "/logs/laravel.log"  # Update to the mounted path
    monitor_logs(log_file_path)
