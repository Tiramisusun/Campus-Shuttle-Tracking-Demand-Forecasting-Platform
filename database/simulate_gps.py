"""Simulate shuttle GPS movement along the Blackrock–Belfield route."""
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("API_BASE", "http://localhost:5000")

# Three stops: Blackrock DART → UCD Smurfit → UCD Belfield Village
STOPS = [
    (53.3015, -6.1775),  # Blackrock DART Station
    (53.3003, -6.1858),  # UCD Smurfit (Carysfort gate)
    (53.3069, -6.2234),  # UCD Belfield Village
]

VEHICLES = [
    {"id": 1, "stop_index": 0, "direction": 1},
    {"id": 2, "stop_index": 1, "direction": 1},
    {"id": 3, "stop_index": 2, "direction": -1},
]

STEPS = 20       # interpolation steps between stops
INTERVAL = 2     # seconds between updates


def interpolate(start, end, steps):
    """Return list of (lat, lng) points between start and end."""
    return [
        (
            start[0] + (end[0] - start[0]) * i / steps,
            start[1] + (end[1] - start[1]) * i / steps,
        )
        for i in range(steps + 1)
    ]


def post_location(vehicle_id, lat, lng):
    try:
        requests.post(
            f"{API_BASE}/api/vehicles/{vehicle_id}/location",
            json={"lat": lat, "lng": lng},
            timeout=3,
        )
    except requests.RequestException:
        pass


def run():
    print(f"Simulating GPS for {len(VEHICLES)} vehicles. Press Ctrl+C to stop.")
    states = [
        {"stop_index": v["stop_index"], "direction": v["direction"], "step": 0, "points": []}
        for v in VEHICLES
    ]

    for i, v in enumerate(VEHICLES):
        state = states[i]
        next_stop = (state["stop_index"] + state["direction"]) % len(STOPS)
        state["points"] = interpolate(STOPS[state["stop_index"]], STOPS[next_stop], STEPS)

    while True:
        for i, v in enumerate(VEHICLES):
            state = states[i]
            lat, lng = state["points"][state["step"]]
            post_location(v["id"], lat, lng)
            print(f"  BUS-{v['id']:03d}  lat={lat:.4f}  lng={lng:.4f}")

            state["step"] += 1
            if state["step"] > STEPS:
                state["step"] = 0
                state["stop_index"] = (state["stop_index"] + state["direction"]) % len(STOPS)
                if state["stop_index"] in (0, len(STOPS) - 1):
                    state["direction"] *= -1
                next_stop = (state["stop_index"] + state["direction"]) % len(STOPS)
                state["points"] = interpolate(STOPS[state["stop_index"]], STOPS[next_stop], STEPS)

        time.sleep(INTERVAL)


if __name__ == "__main__":
    run()
