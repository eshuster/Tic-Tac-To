from flask import jsonify, request
from app import db

from app.models import Game, Board, Cell
from app.game import game

@game.route('/new_game', methods=['POST'])
def new_game():
	try:
		data = request.get_json() or {}

		game = Game()
		game.name = data['name']
		game.create_board()

		db.session.add(game)
		db.session.commit()
		
		return jsonify({"game_id" : game.id, "name" : game.name})
		
	except Exception as e:
		response = jsonify({"error" : str(e)})
		response.status_code = 500

		return response