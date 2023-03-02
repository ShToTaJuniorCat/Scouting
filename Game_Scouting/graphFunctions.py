import firebase_admin
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from firebase_admin import credentials
from firebase_admin import db


def is_team_in_db(team_id):
    ref = db.reference('teams/{}'.format(team_id))
    res = ref.get()
    return res

def graph_per_game(team_id, game_results, y_title, max_y):
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    x_axis = []
    for i in range(len(game_results)):
        x_axis.append(i+1)

    plt.plot(x_axis, game_results, marker = 'o', markersize = 5)
    plt.xlabel('Game Number')
    plt.ylabel(y_title)
    plt.axis([0, len(game_results), 0, max_y])
    plt.title('team ' + str(team_id) + " - " + y_title)
    for i, j in zip(x_axis, game_results):
        plt.text(i, j+1, '({}, {})'.format(i, j))
    plt.draw()
    plt.pause(0.001)

def graph_total_collected_per_game(team_id, all_games, show_graphs):
    game_results = []
    for game in all_games:
        json = all_games[game]
        auto_collected_pieces = json["au_Collected pieces"]

        teleop_floor_collected_pieces = json["te_Pieces collected from floor"]
        teleop_shelf_collected_pieces = json["te_Pieces collected from floor"]
        
        total_pieces = auto_collected_pieces + teleop_floor_collected_pieces + teleop_shelf_collected_pieces
        
        game_results.append(total_pieces)

    if show_graphs:
        graph_per_game(team_id, game_results, 'Pieces Collected', 100)

    return game_results
    

def graph_accuracy_tele_per_game(team_id, all_games, show_graphs):
    game_results = []
    
    for game in all_games:
        json = all_games[game]
        
        teleop_floor_pieces_collected = json['te_Pieces collected from floor']
        teleop_shelf_pieces_collected = json['te_Pieces collected from shelf']

        teleop_collected_total = teleop_floor_pieces_collected + teleop_shelf_pieces_collected

        
        teleop_first_level_score_count = json['te_First level pieces scored']
        teleop_second_level_score_count = json['te_Second level pieces scored']
        teleop_third_level_score_count = json['te_Third level pieces scored']
        
        successful_scored = teleop_first_level_score_count + teleop_second_level_score_count + teleop_third_level_score_count
        
        if (teleop_collected_total < 1):
            teleop_collected_total = 1
        game_results.append(successful_scored / teleop_collected_total * 100)

    if show_graphs:
        graph_per_game(team_id, game_results, f"Accuracy TELEOP (%) - {round(sum(game_results) / len(game_results), 3)}%", 100)

    return game_results

def graph_accuracy_auto_per_game(team_id, current_event):
    game_results = []
    games = db.reference(f"teams/{team_id}/events/{current_event}/gms").get()
        
    for game in games.keys():
        game_json = games[game]

        # Get total pieces collected during auto 
        auto_collected_total = game_json['au_Collected pieces']

        auto_first_level_scored = game_json["au_First level pieces scored"]
        auto_second_level_scored = game_json["au_Second level pieces scored"]
        auto_third_level_scored = game_json["au_Third level pieces scored"]
        
        successful_scored = auto_first_level_scored + auto_second_level_scored + auto_third_level_scored
        
        if (auto_collected_total < 1):
            auto_collected_total = 1
        game_results.append(successful_scored / auto_collected_total * 100)

    graph_per_game(team_id, game_results, 'Accuracy AUTO (%)', 100)

    
def graph_inactive_per_game(team_id, all_games):
    game_results = []
    for game in all_games:
        json = all_games[game]

        # Fortmat: "X sec"
        # Example: "67 sec"
        inactive_time = int(json['ge_Inactive time'].split(" ")[0])

        game_results.append(inactive_time / 150 * 100)

    graph_per_game(team_id, game_results, 'Inactive Time (%)', 100)
