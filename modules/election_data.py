import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def load_states():
    path = os.path.join(BASE_DIR, "data", "states.json")

    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}


def load_deadlines():
    path = os.path.join(BASE_DIR, "data", "deadlines.json")

    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}


def get_state_info(state):
    states = load_states()
    return states.get(state, {
        "registration": "Check local website",
        "id_required": "Varies",
        "poll_hours": "7 AM - 8 PM"
    })


def get_deadline(state):
    deadlines = load_deadlines()
    return deadlines.get(state, {
        "registration_deadline": "Unknown",
        "election_day": "Unknown"
    })