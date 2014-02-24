import random

class Tree:
	root = None

class Player:
	none = 0
	white = 1
	black = 2
	@classmethod
	def other(cls,player):
		if player == Player.black:
			player = Player.white
		elif player == Player.white:
			player = Player.black
		return(player)
	
class Game:
	n = 0 #reicht vielleicht auch wenn die states dimension haben
	def __init__(self,n):
		self.n = n
		self.moves = []
		self.states = []
	@classmethod
	def empty(cls,n):
		new_game = cls(n)
		new_game.states = [State.emptyboard(n)]
		return(new_game)
	@classmethod
	def from_state(cls,state):
		new_game = cls(state.n)
		new_game.states = [state]
		return(new_game)
	def __str__(self):
		return(self.last_state().__str__())
	def set_stone(self,move):
		self.moves.append(move)
		new_state = State.from_state(self.last_state(),move)
		self.states.append(new_state)
	def last_state(self):
		return self.states[len(self.states)-1]

class Move:
	player = Player.none
	coordinates = None
	def __init__(self,player,coordinates):
		self.player=player
		self.coordinates=coordinates
	def skip(self):
		if self.coordinates is None:
			return(True)
		else:
			return(False)

class State: # should be immutable and by reference
	n = 0
	board = [[]]
	def __init__(self,board):
		self.n = len(board)
		self.board = board
	@classmethod
	def from_state(cls,old_state,move):
		if move.skip() == False:
			n=old_state.n
			newboard = [[0]*n for i in range(n)]
			for i in range(n):
				for j in range(n):
					newboard[i][j] = old_state.board[i][j]
			newboard[move.coordinates[0]][move.coordinates[1]] = move.player
			return(cls(newboard))
		else:
			return(old_state)
	@classmethod
	def emptyboard(cls,n):
		newboard = [[0]*n for i in range(n)]
		return(cls(newboard))
	def __str__(self):
		def board_to_str(matrix):
			bstring = ""
			for i in range(len(matrix)):
				for j in range(len(matrix)):
					bstring = bstring + str(matrix[i][j])
				bstring = bstring + "\n"
			return(bstring)
		return(board_to_str(self.board))
	def __hash__(self):
		hashsum = 0
		n = len(self.board)
		for i in range(n):
			for j in range(i):
				if self.board[i][j] == Player.none:
					continue
				elif self.board[i][j] == Player.white:
					hashsum = hashsum+(i+1)*(j+1)*3
				elif self.board[i][j] == Player.black:
					hashsum = hashsum+(i+1)*(j+1)*5
			for j in range(i,n):
				if self.board[i][j] == Player.none:
					continue
				elif self.board[i][j] == Player.white:
					hashsum = hashsum+(i+1)*(j+1)*7
				elif self.board[i][j] == Player.black:
					hashsum = hashsum+(i+1)*(j+1)*11
		return(hashsum)
#	def __cmp__(self,other):
#		return(self.__hash__()-other.__hash__())


#Hilfsfunktionen

def create_from_list(n,list):
		sp = Game.empty(n)
		player = Player.white
		for zug in list:
			sp.set_stone(Move(player,zug))
			player = Player.other(player)
		return sp
	
#durchfuehrung

n = 9

first = Move(Player.black,(2,2))
second = Move(Player.white,(2,3))

go = Game.empty(n)
go.set_stone(first)
go.set_stone(second)

zuege=[(1,1),(1,2),(2,2),(2,1),(8,8),None,None]
speedgame = create_from_list(n,zuege)

##################################################
################# hash-test ######################
##################################################
# m=19
# testspiel = Game.empty(m)
# treffer = False
# count = 0
# while treffer == False:
# 	a = random.randint(0,m-1)
# 	b = random.randint(0,m-1)
# 	c = random.randint(0,2)
# 	testspiel.set_stone(Move(c,(a,b)))
# 	h = testspiel.last_state().__hash__()
# 	for i in range(len(testspiel.states)-2):
# 		if h == testspiel.states[i].__hash__():
# 			print("treffer")
# 			print(testspiel.states[i])
# 			print(testspiel.last_state())
# 			print(count)
# 			print(testspiel.states[i].__hash__())
# 			print(testspiel.last_state().__hash__())
# 			for j in range(m):
# 				for k in range(m):
# 					if testspiel.states[i].board[j][k] == testspiel.last_state().board[j][k]:
# 						continue
# 					else:
# 						treffer = True
# 						print((j,k))
# 	count = count + 1