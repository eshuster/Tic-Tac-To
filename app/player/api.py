from flask import jsonify, request, Flask, json
from app import db
from flask_cors import CORS, cross_origin

from app.models import Game, Board, Cell, Player
from app.player import player

# app = Flask(__name__)
# CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

@player.route('/create_players', methods=['POST'])
@cross_origin()
def create_players():
	try:
		data = request.get_json() or {}

		player_one = Player()
		player_two = Player()
		player_one.username = data['playerOneName']
		player_two.username = data['playerTwoName']

		result_one = player_one.add_to_game(data['gameId'])
		result_two = player_two.add_to_game(data['gameId'])

		if result_one == "Game is Full" or result_two == "Game is Full":
			return jsonify({"error" : "Cannot Add Player To An Already Full Game"})
		if result_one != "Game is Full" and result_two != "Game is Full":
			db.session.add(player_one)
			db.session.add(player_two)
			db.session.commit()

			response = jsonify({"playerOneId" : player_one.id, "playerOneName" : player_one.username, "playerTwoId" : player_two.id, "playerTwoName" : player_two.username })
			response.status_code = 201

			return response
		
	except Exception as e:
		response = jsonify({"error" : str(e)})
		response.status_code = 500

		return response

