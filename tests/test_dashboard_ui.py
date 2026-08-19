import os
import re

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, expect

load_dotenv()

BASE_URL = os.getenv("THINGSBOARD_URL")
USERNAME = os.getenv("THINGSBOARD_USERNAME")
PASSWORD = os.getenv("THINGSBOARD_PASSWORD")


def test_dashboard_ui():
    assert BASE_URL
    assert USERNAME
    assert PASSWORD

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # Open ThingsBoard cloud
        page.goto(BASE_URL, wait_until="domcontentloaded")

        # Loggin to ThingsBoard
        page.get_by_label("Username").fill(USERNAME)
        page.get_by_label("Password").fill(PASSWORD)

        page.get_by_role(
            "button",
            name="Sign in",
            exact=True
        ).click()

        # Wait for application to load
        dashboards = page.get_by_text(
            "Dashboards",
            exact=True
        )

        expect(
            dashboards
        ).to_be_visible(timeout=30000)

        dashboards.click()

        # Open Device Telemetry Dashboard
        dashboard = page.get_by_text(
            "Device Telemetry Dashboard",
            exact=True
        )

        expect(
            dashboard
        ).to_be_visible(timeout=30000)

        dashboard.click()

        # Find dashboard widgets using their visible labels
        temperature_label = page.get_by_text(
            "Temperature",
            exact=True
        ).first

        humidity_label = page.get_by_text(
            "Humidity",
            exact=True
        ).first

        power_label = page.get_by_text(
            "Power Consumption",
            exact=True
        ).first

        # Verify widgets are visible
        expect(
            temperature_label
        ).to_be_visible(timeout=30000)

        expect(
            humidity_label
        ).to_be_visible(timeout=30000)

        expect(
            power_label
        ).to_be_visible(timeout=30000)

        # Locate the corresponding widgets
        temperature_card = temperature_label.locator(
            "xpath=ancestor::div[contains(@class, 'tb-widget')][1]"
        )

        humidity_card = humidity_label.locator(
            "xpath=ancestor::div[contains(@class, 'tb-widget')][1]"
        )

        power_card = power_label.locator(
            "xpath=ancestor::div[contains(@class, 'tb-widget')][1]"
        )

        # Locate the displayed values
        temperature_value = temperature_card.locator(
            "div.tb-value-card-value"
        )

        humidity_value = humidity_card.locator(
            "div.tb-value-card-value"
        )

        power_value = power_card.locator(
            "div.tb-value-card-value"
        )

        expect(
            temperature_value
        ).to_be_visible(timeout=30000)

        expect(
            humidity_value
        ).to_be_visible(timeout=30000)

        expect(
            power_value
        ).to_be_visible(timeout=30000)

        # Capture initial values
        temperature_before = temperature_value.inner_text()
        humidity_before = humidity_value.inner_text()
        power_before = power_value.inner_text()

        print("Initial Temperature:", temperature_before)
        print("Initial Humidity:", humidity_before)
        print("Initial Power Consumption:", power_before)

        # Wait for new telemetry
        page.wait_for_timeout(5000)

        # Capture updated values
        temperature_after = temperature_value.inner_text()
        humidity_after = humidity_value.inner_text()
        power_after = power_value.inner_text()

        print("Updated Temperature:", temperature_after)
        print("Updated Humidity:", humidity_after)
        print("Updated Power Consumption:", power_after)

        # Verify that telemetry is updating
        assert (
            temperature_before != temperature_after
            or humidity_before != humidity_after
            or power_before != power_after
        ), "Telemetry values did not update within 5 seconds"

        # Extract numeric values
        temperature_number = float(
            re.search(
                r"-?\d+(\.\d+)?",
                temperature_after
            ).group()
        )

        humidity_number = float(
            re.search(
                r"-?\d+(\.\d+)?",
                humidity_after
            ).group()
        )

        power_number = float(
            re.search(
                r"-?\d+(\.\d+)?",
                power_after
            ).group()
        )

        # Validate acceptable ranges
        assert 15 <= temperature_number <= 40, (
            f"Temperature out of range: "
            f"{temperature_number} °C"
        )

        assert 0 <= humidity_number <= 100, (
            f"Humidity out of range: "
            f"{humidity_number} %"
        )

        assert 0 <= power_number <= 200, (
            f"Power Consumption out of range: "
            f"{power_number} kW"
        )

        # Screenshot evidence
        page.screenshot(
            path="evidence/device_telemetry_dashboard.png",
            full_page=True
        )

        browser.close()