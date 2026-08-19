import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("THINGSBOARD_URL")
USERNAME = os.getenv("THINGSBOARD_USERNAME")
PASSWORD = os.getenv("THINGSBOARD_PASSWORD")
DEVICE_ID = os.getenv("DEVICE_ID")


def test_get_device_telemetry():
    assert BASE_URL
    assert USERNAME
    assert PASSWORD
    assert DEVICE_ID

    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "username": USERNAME,
            "password": PASSWORD
        },
        timeout=10
    )

    assert login_response.status_code == 200

    token = login_response.json()["token"]

    headers = {
        "X-Authorization": f"Bearer {token}"
    }

    telemetry_url = (
        f"{BASE_URL}/api/plugins/telemetry/DEVICE/"
        f"{DEVICE_ID}/values/timeseries"
    )

    telemetry = None

    for _ in range(3):
        response = requests.get(
            telemetry_url,
            headers=headers,
            timeout=10
        )

        assert response.status_code == 200

        telemetry = response.json()

        if all(
            key in telemetry and telemetry[key]
            for key in [
                "temperature",
                "humidity",
                "powerConsumption"
            ]
        ):
            break

        time.sleep(2)

    assert telemetry is not None

    print("Telemetry response:", telemetry)

    for key in [
        "temperature",
        "humidity",
        "powerConsumption"
    ]:
        assert key in telemetry
        assert isinstance(telemetry[key], list)
        assert len(telemetry[key]) > 0
        value = telemetry[key][0]["value"]
        assert isinstance(float(value), float)