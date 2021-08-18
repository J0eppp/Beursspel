from types import resolve_bases
from flask import jsonify, request, Response, g
import json
from .middleware import login_required

# Import the BluePrint from the main file
from . import main
v1bp = main.v1bp

from database import database

@v1bp.route("/games", methods=["POST"])
@login_required
def games_post():
	username = g.user.user_name
	if username != "Admin":
		return jsonfiy({ "error": "you are not authorised for this action" }), 401

	# Create a game
	game = database.Game(game_round_number=0)
	game.new_round()


	session = database.Session()
	session.add(game)
	session.commit()

	# session.close()

	return jsonify(game.serialize), 201

@v1bp.route("/games", methods=["GET"])
@login_required
def games_get():
	session = database.Session()
	res = [item.serialize for item in database.get_games(session)]
	# session.close()
	return jsonify(res), 200

@v1bp.route("/games/join", methods=["POST"])
@login_required
def games_join_post():
	game_id = request.json.get("id")
	session = database.Session()
	game = database.get_game_by_id(session, game_id)
	if game == None:
		return jsonify({ "error": "there is no game with this game_id" }), 400

	user = g.user
	if database.get_player_by_user_id(session, user.user_id) != None:
		return jsonify({ "error": "you are already in this game" }), 400

	player = database.Player(game_id=game_id, player_money=0, player_ready=False)
	database.add_player(session, player)
	return jsonify(player.serialize), 201