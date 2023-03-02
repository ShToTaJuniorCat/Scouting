import graphFunctions as gf
import firebase_admin
import matplotlib.pyplot as plt
from firebase_admin import credentials
from firebase_admin import db
from pyperclip import copy
import re

cred = credentials.Certificate('./credentials.json')
app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://everscout-3c93c.firebaseio.com/'})
print("Connection OK")
# End of Initiation

"""
Possible usage when scouting on non qualification games.
Match codes are like used in the The Blue Alliance API.
"""
GAME_NUM_START = "rf"


while True:
    # Get ID for team to scout
    while True:
        print("Enter team id to show stats for:")
        team_id = int(input())

        team_exists = gf.is_team_in_db(team_id)

        # Team doesn't exist in the database
        if team_exists == None:
            print("Could not find any data related to the team")
            continue
        
        break


    # Does the user want to see graphs?
    graphs = ""
    while graphs != "1" and graphs != "0":
        graphs = input("Show graphs? 1 for yes, 0 for no: ")

    graphs = bool(int(graphs))


    def avg_balls_in(all_collected, accuracy_per_game):
        scored_pieces = [(accuracy_per_game[i]/100) * all_collected[i] for i in range(len(accuracy_per_game))]
        return round(sum(scored_pieces) / len(scored_pieces), 3)


    def first_level_pieces_by_game(game_num):
        game = all_games_json[str(game_num)]
        
        auto_first_level = game["au_Collected pieces"]
                
        tele_first_level = game["te_First level pieces score"]
        
        return auto_first_level + tele_first_level


    def get_game_number(game):
        return int(re.split("(\d+)", game[0])[1])


    def graph_total_collected_from_json(game_json):
        auto_collected_pieces = game_json["au_Collected pieces"]

        teleop_floor_collected_pieces = game_json["te_Pieces collected from floor"]
        teleop_shelf_collected_pieces = game_json["te_Pieces collected from shelf"]

        total_pieces = auto_collected_pieces + teleop_floor_collected_pieces + teleop_shelf_collected_pieces

        return total_pieces


    current_event = db.reference("settings/current_event/key").get()
    all_games_json = db.reference(f"teams/{team_id}/events/{current_event}/gms").get()

    # sort games by game number
    all_games_json = dict(sorted(all_games_json.items(), key=get_game_number))
    keys = list(all_games_json.keys())

    for key in keys:
        all_games_json[key[4:]] = all_games_json.pop(key) # re.split("(\d+)", key)[1]] = all_games_json.pop(key)

    #graph_it()

    # 6 graphs total
    collected_pieces_per_game = gf.graph_total_collected_per_game(team_id, all_games_json, graphs)
    accuracy_per_game = gf.graph_accuracy_tele_per_game(team_id, all_games_json, graphs)

    if graphs:
        gf.graph_accuracy_auto_per_game(team_id, current_event)
        gf.graph_inactive_per_game(team_id, all_games_json)

    last_game_num = max([int(i) for i in list(all_games_json.keys())])


    print("\n\n-------------------")

    info = """Games played: """ + str(len(all_games_json)) + """
    Average pieces collected: """ + str(round(sum(collected_pieces_per_game) / len(collected_pieces_per_game), 3)) + """
    Average pieces scored: """ + str(avg_balls_in(collected_pieces_per_game, accuracy_per_game)) + """
    Scoring percentage: """ + str(round(sum(accuracy_per_game) / len(accuracy_per_game), 3)) + """%
    Last game numer: """ + str(last_game_num) + """
    Pieces collected: """ + str(graph_total_collected_from_json(all_games_json[str(last_game_num)])) + """
    Pieces scored: """ + str((graph_total_collected_from_json(all_games_json[str(last_game_num)]) / 100) * accuracy_per_game[len(accuracy_per_game) - 1])
    copy(info)
    print(info)

    print("-------------------\n\n\n\n\n\n\n\n\n\n")

    break
