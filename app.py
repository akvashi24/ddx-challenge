from flask import Flask

# Part 1

app = Flask(__name__)

# ? Unclear if JSON file would be an object or list at the top level
# Also unclear what should happen in the event of a tie, currently takes last candidate
data = {
    "Pennsylvania": {
        "Chester": {
            "Democrats": {"Humphrey": 10000, "McGovern": 5000},
            "Republicans": {"Nixon": 20000, "Ashbrook": 200, "McCloskey": 100},
        },
        "Allegheny": {
            "Democrats": {"Humphrey": 10000, "McGovern": 5000},
            "Republicans": {"Nixon": 7500, "Ashbrook": 5000},
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
    return result

# Part 2.

# select county, party, candidate, max(votes) from results group by party, county;

# Part 3: Say the data provider tells you JSON files will be arriving once an hour with incremental vote count updates.
# You are tasked with architecting a system to load those files into the table from part 2 once they arrive.
# In a paragraph or two, please answer the following
# ● What does your ideal architecture look like to accomplish this?
# ● What questions do you still need answered in order to build the system? 

# A system that could update the table from part 2 periodically would not have to be very complicated to work effectively.
# I would make some changes to the table schema first, and then set up an infrastructure for ingesting, cleaning, and
# inserting the data.  First, I would need to understand how the files are coming in.  This could be via a REST API,
# a file upload to a storage service like S3, direct transfer via SFTP, or even something as basic as email attachments.
# I would also want to understand the fidelity of these files - is it possible or even likely that they would need to be
# edited or amended?  Another question I would have is about reads and writes.  It's noted that writes would happen every hour,
# but how many counties would be updating on the hour?  How many users would be attempting to read and how often?  This 
# would all affect the infrastructure required to host a solution and certain implementation details about the availability
# of the data.



