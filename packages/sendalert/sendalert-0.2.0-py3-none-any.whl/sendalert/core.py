import os
import requests

class Notifier:
    def __init__(self):
        self.api_key = os.environ.get("SENDALERT_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be set as SENDALERT_API_KEY environment variable")
        self.base_url = "https://api.sendalert.io/v1/alert"
        self.default_project = os.environ.get("SENDALERT_PROJECT", "default")

    def send_alert(self, project, mode, text):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "project": project or self.default_project,
            "mode": mode,
            "text": text
        }
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            print("Notification sent successfully")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending notification: {e}")
            return False

def sendalert(text, project=None, mode="default"):
    notifier = Notifier()
    return notifier.send_alert(project, mode, text)

default_api_key = os.environ.get("SENDALERT_API_KEY")

globals()['sendalert'] = sendalert
