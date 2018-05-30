from flask import jsonify, request
from app import db

from app.models import Game, Board, Cell, Player
from app.board import board

@board.route('/check_for_winner/<int:board_id>/<int:player_id>', methods=['GET'])
def check_for_winner(board_id, player_id):
	try:
		board = Board.query.get_or_404(board_id)
		player = Player.query.get_or_404(player_id)

		check_result = board.check_for_winner(player)
		
		if check_result == True:
			return jsonify({"winner" : True})
		else:
			return jsonify({"winner" : False})
			
	except Exception as e:
		response = jsonify({"error" : str(e)})
		response.status_code = 404

		return response


@board.route('/select_position', methods=['POST'])
def select_position():
	try:
		data = request.get_json() or {}
		board = Board.query.get(data['board_id'])
		game = board.game
		player = Player.query.get_or_404(data['player_id'])

		if game.active == True:
			if str(board.last_player) != str(player.id):			
				cell = Cell.query.get_or_404(data['cell_id'])

				# if cell.player_id is None:
				if cell.player is None:
					cell.player = player
					cell.player_id = player.id
					cell.board = board

					board.last_player = player.id
					check_result = board.check_for_winner(player);

					if check_result == True:
						game.active = False

						return jsonify({"winner" : True, "board" : repr(game.board.cell)})
					else:
						return jsonify({"winner" : False, "board" : repr(game.board.cell)})

					db.session.commit()
				else:
					return jsonify({"error" : "Position Already Selected"})

			if str(board.last_player) == str(player.id):
				return jsonify({"error" : "Other Player's Turn"})
		else:
			return jsonify({"error" : "Game Is No Longer Active"})

	except Exception as e:
		response = jsonify({"error" : str(e)})
		response.status_code = 404

		return response













