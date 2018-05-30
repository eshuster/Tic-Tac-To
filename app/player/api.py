from flask import jsonify, request
from app import db

from app.models import Game, Board, Cell, Player
from app.player import player

@player.route('/create_player', methods=['POST'])
def create_player():
	try:
		data = request.get_json() or {}

		player = Player()
		player.username = data['username']
		player.symbol = data['symbol']

		result = player.add_to_game(data['game_id'])

		if result == "Game is Full":
			return jsonify({"error" : "Cannot Add Player To An Already Full Game"})
		else:
			db.session.add(player)
			db.session.commit()

			response = jsonify({"player_id" : player.id, "username" : player.username, "symbol" : player.symbol})
			response.status_code = 201

			return response
		
	except Exception as e:
		response = jsonify({"error" : str(e)})
		response.status_code = 500

		return response
