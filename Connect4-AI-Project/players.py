from cmath import inf
from codecs import backslashreplace_errors
from copy import copy, deepcopy
from os import getenv
import random
import time
from turtle import down
import pygame
import math

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):
	

	def backSlashDiag(self, board, row, col, player, inARow):
		tally = 0
		temp_inARow = inARow
		temp_row = row
		temp_col = col
		while(temp_row-1 > -1 and temp_col-1 > -1 and temp_inARow > 0 and board[temp_row-1][temp_col-1] == player):
			#Remove tally not the point of it here
			tally += 1
			temp_inARow -= 1
			temp_row -= 1
			temp_col -= 1
		temp_inARow = inARow
		temp_row = row
		temp_col = col
		while(temp_row+1 < 6 and temp_col+1 < 7 and board[temp_row+1][temp_col+1] == player):
			tally += 1
			temp_inARow -= 1
			temp_row += 1
			temp_col += 1
		
		return tally
	
	def forwardSlashDiag(self, board, row, col, player, inARow):
		tally = 0
		temp_inARow = inARow
		temp_row = row
		temp_col = col
		while(temp_row-1 > -1 and temp_col+1 < 7 and temp_inARow > 0 and board[temp_row-1][temp_col+1] == player):
			tally += 1
			temp_inARow -= 1
			temp_row -= 1
			temp_col += 1
		
		temp_inARow = inARow
		temp_row = row
		temp_col = col
		while(temp_row+1 < 6 and temp_col-1 > -1 and temp_inARow > 0 and board[temp_row+1][temp_col-1] == player):
			tally += 1
			temp_inARow -= 1
			temp_row += 1
			temp_col -= 1
		
		return tally
	
	def vertical(self, board, row, col, player, inARow):
		tally = 0
		temp_row = row
		while(temp_row+1 < 6 and board[temp_row+1][col] == player):
			count += 1
			temp_row += 1
			print("row-")
		
		temp_row = row
		while(temp_row-1 > -1 and board[temp_row-1][col] == player):
			count += 1
			temp_row -= 1
			print("row-")
		
		return count
	
	def horizontal(self, board, row, col, player, inARow):
		count = 1
		temp_col = col
		while(temp_col+1 < 7 and board[row][temp_col+1] == player):
			count += 1
			temp_col += 1
		
		temp_col = col
		while(temp_col-1 > -1 and board[row][temp_col-1] == player):
			count += 1
			temp_col -= 1
		
		return count
	
	def eval(self, env):
		copy = deepcopy(env)
		
		#Who am I? Player1 or Player2?
		if self.position == 1:
			opponent = 2
		elif self.position == 2:
			opponent = 1
		
		#Start counting
		myTwos = self.inARowCheck(copy, self.position, 2)
		myThrees = self.inARowCheck(copy, self.position, 3)
		myFours = self.inARowCheck(copy, self.position, 4)

		opponentTwos = self.inARowCheck(copy, opponent, 2)
		opponentThrees = self.inARowCheck(copy, opponent, 3)
		opponentFours = self.inARowCheck(copy, opponent, 4)

		#Tally things up
		total = 8*(myFours - opponentFours) + 4*(myThrees - opponentThrees) + 2*(myTwos - opponentTwos)
		return total

	def inARowCheck(self, board, player, inARow):
		for row in range(6):
			for col in range(7):
				if board[row][col] == player:
					#Check left down diagonal
					self.backSlashDiag(board, row, col, player, inARow)
					#Check left up diagonal
					self.forwardSlashDiag(board, row, col, player, inARow)
					#Check vertical
					self.vertical(board, row, col, player, inARow)
					#Check horizontals
					self.horizontal(board, row, col, player, inARow)
		
	
	def play(self, env, move):

		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]
		
		self.eval(env)

	def minimax():
		print("Chunk")

class alphaBetaAI(connect4Player):

	def play(self, env, move):
		pass


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




