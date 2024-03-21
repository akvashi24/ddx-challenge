from flask import Flask
from pprint import pprint

app = Flask(__name__)

# ? Unclear if JSON file would be an object or list at the top level
# Also unclear what should happen in the event of a tie, currently replaces 
data = {
    "Pennsylvania": {
        "Chester": {
            "Democrats": {"Humphrey": 10000, "McGovern": 5000},
            "Republicans": {"Nixon": 20000, "Ashbrook": 200, "McCloskey": 100},
        },
        "Allegheny": {
            "Democrats": {"Humphrey": 10000, "McGovern": 8090},
            "Republicans": {"Nixon": 15000, "Ashbrook": 400, "McCloskey": 7000},
        }
    },
    "New Jersey": {
        "Morris": {
            "Democrats": {"Humphrey": 4000, "McGovern": 7000},
            "Republicans": {"Nixon": 18000, "Ashbrook": 4000, "McCloskey": 6000},
        }
    },
}


def get_county_winner(county_data):
    # Gets winner of a single party in a county
    winning_vote_count = 0
    winner = "No winner found"
    for candidate, current_vote_count in county_data.items():
        if current_vote_count > winning_vote_count:
            winning_vote_count = current_vote_count
            winner = candidate
    return winner


def get_state_winners(state_data):
    result = {}
    for county_name, county_data in state_data.items():
        county_winners = {}
        county_winners["Democrat"] = get_county_winner(county_data["Democrats"])
        county_winners["Republican"] = get_county_winner(county_data["Republicans"])
        result[county_name] = county_winners
    return result


@app.route("/winners")
def winners_by_state():
    result = {}
    for state, race in data.items():
        result[state] = get_state_winners(race)
    pprint(result)
    return result
