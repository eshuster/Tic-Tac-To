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
	# Returns the id if the set contains the same elements
	def check_rows_and_columns(self, board):
		# print("*** Rows and Columns****")
		# print(board)
		# print("*******"*10)
		for row in board:
			if len(set(row)) == 1:
				return row[0]
		return 0

	# Checks the game_board sent from check_for_winner if check_rows_and_columns returns 0 
	def check_diagonals(self, board, player):
		# print("*** check_diagonals ****")
		# print(board)
		# print("*******"*10)

		if len(set([board[i][i] for i in range(len(board))])) == 1:
			return board[0][0]

			if player.id == board[0][0]:
				return True

		if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
			if player.id == board[0][len(board)-1]:
				return True

		return False

	def check_for_winner(self, player):
		board = []
		row = [] 

		index = 0
		#  Creates the game_board forming an array comprised of arrays with length 9
		# [[1,2, 3, 4...], [10, 11, 12, 13...], [19, 20, 21, 21...], ...]
		while index < len(self.cell):		
			# print(self.cell[index])	
			if (index + 1) % 9 == 0 and index != 0:
				# if self.cell[index].player_id:
				row.append(self.cell[index].player_id)
				board.append(row)
				row= []
			else:
				# if self.cell[index].player_id:
				row.append(self.cell[index].player_id)

			index = index+1

		print(board)
	    # transposition to check rows, then columns
		for new_board in [board, np.transpose(board)]:
			# print("new_board")
			# print(new_board)
			# print("new_board")
			result = self.check_rows_and_columns(new_board)
			# If the result of check_rows_and_columns is not a 0 and maches the Player id then that Player has WON
			if result == player.id:
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
 	
	def toJSON(self):
		return {'cell_id': self.id, 'cell_position': self.position, 'board_id' : self.board_id, 'player_id' : self.player_id, 'game_id' : self.board.game_id, 'game_name' : self.board.game.name}

class Player(db.Model):
	
	id = db.Column(db.Integer, primary_key=True)
	cell = db.relationship('Cell', back_populates='player')
	username = db.Column(db.String(60), index=True)

	game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
	game = db.relationship('Game', back_populates='player', foreign_keys=[game_id])

	# symbol = db.Column(db.String(60), index=True)

	def add_to_game(self, game_id):
		game = Game.query.get_or_404(game_id)
	
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















