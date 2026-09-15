import requests

def send_gesture(name, host="http://127.0.0.1:5000"):
    try:
        response = requests.post(
            f"{host}/api/gesture/send",
            json={"gesture": name},
            timeout=1
        )
        if response.status_code == 200:
            print(f"Gesture Sent : {name}")
            return True
    except requests.exceptions.RequestException:
        print("Backend Offline")
    return False
