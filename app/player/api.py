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

		db.session.add(player)
		db.session.commit()

		response = jsonify({"data" : repr(player)})
		response.status_code = 201

		return response
		
	except Exception as e:
		response = jsonify({"error" : str(e)})
		response.status_code = 500

		return response
