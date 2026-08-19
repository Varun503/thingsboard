import os
import time
import random
import requests

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("THINGSBOARD_URL")
DEVICE_TOKEN = os.getenv("DEVICE_TOKEN")

assert BASE_URL, "THINGSBOARD_URL is not set"
assert DEVICE_TOKEN, "DEVICE_TOKEN is not set"


while True:

    telemetry = {
        "temperature": round(random.uniform(20, 30), 1),
        "humidity": round(random.uniform(50, 70), 1),
        "powerConsumption": round(random.uniform(100, 140), 1)
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/{DEVICE_TOKEN}/telemetry",
        json=telemetry,
        timeout=10
    )

    print(
        f"Status: {response.status_code} | "
        f"Telemetry: {telemetry}"
    )

    response.raise_for_status()

    time.sleep(5)