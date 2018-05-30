from app import db
import numpy as np

# ONE Game has ONE Board and ONE Board Has MANY Cells
# ONE Cell Has ONE Player

class Game(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), index=True, unique=True)
	board = db.relationship('Board', back_populates='game', uselist=False)
	active = db.Column(db.Boolean, default=False)
	player = db.relationship('Player', back_populates='game')

	def create_board(self):
		board = Board()
		board.game = self
		board.last_player = None
		board.create_cells()

	def __repr__(self):
		return '<Game: {}>'.format(self.id)


class Board(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	cell = db.relationship('Cell', back_populates='board')
	game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
	game = db.relationship('Game', back_populates='board', foreign_keys=[game_id])
	last_player = db.Column(db.String(60), nullable=True)

	# Creates 81 entries into the Cell table to represent a 9 x 9 tic tac to board
	def create_cells(self):
		for pos in range(1, 82):
			cell = Cell()
			cell.board = self 
			cell.position = pos
			db.session.add(cell)
			db.session.commit()

	# Checks the game_board sent from check_for_winner
	# Returns the symbol if the set contains the same elements
	def check_rows_and_columns(self, board):
		for row in board:
			if len(set(row)) == 1:
				return row[0]
		return 0

	# Checks the game_board sent from check_for_winner if check_rows_and_columns returns 0 
	def check_diagonals(self, board, player):
		if len(set([board[i][i] for i in range(len(board))])) == 1:
			return board[0][0]

			if player.symbol == board[0][0]:
				return True

		if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
			if player.symbol == board[0][len(board)-1]:
				return True

		return False

	def check_for_winner(self, player):
		board = []
		row = []

		index = 0
		#  Creates the game_board forming an array comprised of arrays with length 9
		# [[1,2, 3, 4...], [10, 11, 12, 13...], [19, 20, 21, 21...], ...]
		while index < len(self.cell):
			
			if (index + 1) % 9 == 0 and index != 0:
				if self.cell[index].player:
					row.append(self.cell[index].player.symbol)
					board.append(row)
					row= []
			else:
				if self.cell[index].player:
					row.append(self.cell[index].player.symbol)

			index = index+1

	    # transposition to check rows, then columns
		for new_board in [board, np.transpose(board)]:
			result = self.check_rows_and_columns(new_board)
			# If the result of check_rows_and_columns is not a 0 and maches the Player symbol then that Player has WON
			if result == player.symbol:
				return True
		return self.check_diagonals(board, player)

	def __repr__(self):
		return '<Board: {}>'.format(self.id)


class Cell(db.Model):

	id = db.Column(db.Integer, primary_key=True)	
	board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
	player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
	board = db.relationship('Board', back_populates='cell', foreign_keys=[board_id, player_id])
	player = db.relationship('Player', back_populates='cell', foreign_keys=[board_id, player_id])
	position = db.Column(db.Integer)

	def __repr__(self):
		return "{cell_id: %s,  cell_position: %s, board_id: %s, player_id: %s}" % (self.id, self.position, self.board_id, self.player_id)
 

class Player(db.Model):
	
	id = db.Column(db.Integer, primary_key=True)
	cell = db.relationship('Cell', back_populates='player')
	symbol = db.Column(db.String(60), index=True, unique=True)
	username = db.Column(db.String(60), index=True, unique=True)

	game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
	game = db.relationship('Game', back_populates='player', foreign_keys=[game_id])

	def add_to_game(self, game_id):
		game = Game.query.get_or_404(game_id)
		print("----" * 8)
		print(game.player)
		print("----" * 8)

		if len(game.player) < 2:
			self.game = game
			db.session.commit()
		else:
			return "Game is Full"

		if len(game.player) == 2:
			game.active = True
			db.session.commit()

	def __repr__(self):
		return '<Player: {}>'.format(self.username)















