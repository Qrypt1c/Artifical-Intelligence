from cmath import inf
from codecs import backslashreplace_errors
from copy import copy, deepcopy
from os import getenv
from pickle import TRUE
import random
import time
from turtle import down
from typing import Counter
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
		temp_inARow = inARow-1
		temp_row = row
		temp_col = col
		while(temp_row-1 > -1 and temp_col-1 > -1 and temp_inARow > 0 and board[temp_row-1][temp_col-1] == player):
			temp_inARow -= 1
			temp_row -= 1
			temp_col -= 1
		if temp_inARow == 0:
			tally = 1
		
		#Avoid double counting
		#temp_inARow = inARow
		#temp_row = row
		#temp_col = col
		#while(temp_row+1 < 6 and temp_col+1 < 7 and temp_inARow > 0 and board[temp_row+1][temp_col+1] == player):
		#	temp_inARow -= 1
		#	temp_row += 1
		#	temp_col += 1
		#if temp_inARow == 0:
		#	tally += 1
		
		return tally
	
	def forwardSlashDiag(self, board, row, col, player, inARow):
		tally = 0
		temp_inARow = inARow-1
		temp_row = row
		temp_col = col
		while(temp_row-1 > -1 and temp_col+1 < 7 and temp_inARow > 0 and board[temp_row-1][temp_col+1] == player):
			temp_inARow -= 1
			temp_row -= 1
			temp_col += 1
		if temp_inARow == 0:
			tally = 1
		
		#Avoid double counting
		#temp_inARow = inARow
		#temp_row = row
		#temp_col = col
		#while(temp_row+1 < 6 and temp_col-1 > -1 and temp_inARow > 0 and board[temp_row+1][temp_col-1] == player):
		#	temp_inARow -= 1
		#	temp_row += 1
		#	temp_col -= 1
		#if temp_inARow == 0:
		#	tally += 1
		
		return tally
	
	def vertical(self, board, row, col, player, inARow):
		tally = 0
		temp_inARow = inARow-1
		temp_row = row
		while(temp_row+1 < 6 and temp_inARow > 0 and board[temp_row+1][col] == player):
			temp_inARow -= 1
			temp_row += 1
			#print("row-")
		if temp_inARow == 0:
			tally = 1
			#print("Tally changed vertical!")
		
		#Avoid double counting
		#temp_inARow = inARow
		#temp_row = row
		#while(temp_row-1 > -1 and board[temp_row-1][col] == player):
		#	temp_inARow -= 1
		#	temp_row -= 1
		#	print("row-")
		#if temp_inARow == 0:
		#	tally += 1
		
		return tally
	
	def horizontal(self, board, row, col, player, inARow):
		tally = 0
		temp_inARow = inARow-1
		temp_col = col
		while(temp_col+1 < 7 and temp_inARow > 0 and board[row][temp_col+1] == player):
			temp_inARow -= 1
			temp_col += 1
		if temp_inARow == 0:
			tally = 1
		
		#Avoid double counting
		#temp_col = col
		#while(temp_col-1 > -1 and board[row][temp_col-1] == player):
		#	count += 1
		#	temp_col -= 1
		
		return tally
	
	def eval(self, env):
		copy = deepcopy(env)

		#Start counting
		myTwos = self.inARowCheck(copy.board, self.position, 2)
		myThrees = self.inARowCheck(copy.board, self.position, 3)
		myFours = self.inARowCheck(copy.board, self.position, 4)
		print("My twos: ", myTwos, " threes: ", myThrees, " fours: ", myFours)

		opponentTwos = self.inARowCheck(copy.board, self.opponent.position, 2)
		opponentThrees = self.inARowCheck(copy.board, self.opponent.position, 3)
		opponentFours = self.inARowCheck(copy.board, self.opponent.position, 4)
		print("Opponent twos: ", opponentTwos, " threes: ", opponentThrees, " fours: ", opponentFours)

		#Tally things up
		total = 8*(myFours - opponentFours) + 4*(myThrees - opponentThrees) + 2*(myTwos - opponentTwos)
		print("Total: ", total)
		return total

	def inARowCheck(self, board, player, inARow):
		counter = 0
		for row in range(6):
			for col in range(7):
				if board[row][col] == player:
					#print("[Row][Col]: [",row,"][",col,"]" )
					#Check left down diagonal
					counter += self.backSlashDiag(board, row, col, player, inARow)
					#Check left up diagonal
					counter += self.forwardSlashDiag(board, row, col, player, inARow)
					#Check vertical
					counter += self.vertical(board, row, col, player, inARow)
					#Check horizontals
					counter += self.horizontal(board, row, col, player, inARow)
		return counter

	def lastPlayerCalculator(self, env):
		if len(env.history[0]) > len(env.history[1]):
			print("The last player was player 1")
			return 1
		else:
			print("The last player was player 2")
			return 2

	def lastMoveCalculator(self,env):
		if len(env.history[0]) == 0:
			#no one has played yet assume player 2 played last
			return 0
		elif len(env.history[0]) > len(env.history[1]):
			#player 1 played last
			return env.history[0][len(env.history[0])-1]
		else:
			#player 1 and player 2 have same length so player 2 played last
			return env.history[1][len(env.history[1])-1]
	
	def play(self, env, move):
		if self.position == 1 and len(env.history[0]) == 0 and len(env.history[1]) == 0:
			move[:] = [3]
		else:
			move[:] = [self.minimax(env, 1, TRUE)[0]]
	
	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
	
	def minimax(self, env, depth, maximizingPlayer):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		endNode = env.gameOver(self.lastMoveCalculator(env), self.lastPlayerCalculator(env))
		if depth == 0 or endNode:
			if endNode:
				if self.lastPlayerCalculator == self.position:
					return (None, 100000000)
				elif self.lastPlayerCalculator == self.opponent.position:
					return (None, -100000000)
				else:
					return (None, 0)
			else:
				return (None, self.eval(env))
		if maximizingPlayer:
			val = -math.inf
			move_col = -math.inf
			for col in indices:
				row = env.topPosition[col]
				copy = deepcopy(env)
				self.simulateMove(copy, col, self.position)
				score = self.minimax(copy, depth-1, False)[1]
				if score > val:
					val = score
					move_col = col
			return (move_col, val)
		else:
			val = math.inf
			move_col = math.inf
			for col in indices:
				row = env.topPosition[col]
				copy = deepcopy(env)
				self.simulateMove(copy, col, self.opponent.position)
				score = self.minimax(copy, depth-1, True)[1]
				if score < val:
					val = score
					move_col = col
			return (move_col, val)
					

		

			


		

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




