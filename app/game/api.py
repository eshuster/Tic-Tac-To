from flask import jsonify, request, Flask, json
from app import db

from flask_cors import CORS, cross_origin

from app.models import Game, Board, Cell
from app.game import game

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@game.route('/new_game', methods=['POST'])
@cross_origin()
def new_game():

	try:
		data = request.get_json() or {}

		game = Game()
		game.name = data['name']
		game.create_board()

		db.session.add(game)
		db.session.commit()
		
		jsonStr = json.dumps([e.toJSON() for e in game.board.cell])

		return jsonStr
	
	except Exception as e:
		response = jsonify({"error" : str(e)})
		response.status_code = 500

		return response


