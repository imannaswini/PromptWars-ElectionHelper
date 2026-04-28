from modules.engine import ElectionEngine

# Keep old class name so app.py still works
class ElectionLogicEngine(ElectionEngine):
    pass


def get_election_timeline():
    return {
        "Registration Deadline": "October 10, 2026",
        "Mail-in Ballot Request": "October 20, 2026",
        "Early Voting Starts": "October 25, 2026",
        "Election Day": "November 3, 2026"
    }