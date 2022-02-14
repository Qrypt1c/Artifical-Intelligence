from cmath import inf
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

	def in_a_row_counter(self, env):
		print("no")
	
	def eval(self, env, move):
		
		my_fours = opp_fours = my_threes = opp_threes = my_twos = opp_twos = my_ones = opp_ones = 0
		
		fours = my_fours - opp_fours
		if (fours > 0):
			print("Value of game: ", inf)
			return inf
		elif (fours < 0):
			print("Value of game: ", -inf)
			return -inf
		else:
			threes = 10000*(my_threes - opp_threes)
			twos = 100*(my_twos - opp_twos)
			ones = my_ones - opp_ones
			val = threes + twos + ones
			print("Value of game: ", val)
		return val
	
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
		
		# INSERT BS HERE
		copy = deepcopy(env)

		for row in range(6):
			for col in range(7):
				#Initializations
				downSlopeLTRCount = 0
				upSlopeLTRCount = 0
				upDownCount = 0
				horizontalCount = 0
				temp = 0
				
				if copy.board[row][col] == 1:
					#Checking for in a row from down slope left to right
					while(copy.board[row-1][col-1] == 1):
						temp += 1
					downSlopeLTRCount = temp + 1
					temp = 0
					while(copy.board[row+1][col+1] == 1):
						temp += 1
					downSlopeLTRCount = downSlopeLTRCount + temp

					#Now checking for in a row from up slope left to right
					while(copy.board[row-1][col+1] == 1):
						temp += 1
					upSlopeLTRCount = temp + 1
					temp = 0
					while(copy.board[row+1][col-1] == 1):
						temp += 1
					upSlopeLTRCount = upSlopeLTRCount + temp
					
					#Now checking for in a col up and down
					temp = 0
					while(copy.board[row+1][col] == 1):
						temp += 1
					upDownCount = temp + 1
					temp = 0
					while(copy.board[row-1][col] == 1):
						temp += 1
					upDownCount = upDownCount + temp

					#Now checking for in a row side to side
					temp = 0
					while(copy.board[row][col+1] == 1):
						temp += 1
					horizontalCount = temp + 1
					temp = 0
					while(copy.board[row][col-1] == 1):
						temp += 1
					horizontalCount = horizontalCount + temp

					#Tally results
					if downSlopeLTRCount == 1:
						ones = ones + downSlopeLTRCount
					elif downSlopeLTRCount == 2:
						twos = twos + downSlopeLTRCount
					elif downSlopeLTRCount == 3:
						threes = threes + downSlopeLTRCount
					else:
						fours = fours + downSlopeLTRCount
					
					if upSlopeLTRCount == 1:
						ones = ones + upSlopeLTRCount
					elif upSlopeLTRCount == 2:
						twos = twos + upSlopeLTRCount
					elif upSlopeLTRCount == 3:
						threes = threes + upSlopeLTRCount
					else:
						fours = fours + upSlopeLTRCount

					if upDownCount == 1:
						ones = ones + upDownCount
					elif upDownCount == 2:
						twos = twos + upDownCount
					elif upDownCount == 3:
						threes = threes + upDownCount
					else:
						fours = fours + upDownCount

					if horizontalCount == 1:
						ones = ones + horizontalCount
					elif horizontalCount == 2:
						twos = twos + horizontalCount
					elif horizontalCount == 3:
						threes = threes + horizontalCount
					else:
						fours = fours + horizontalCount
					
				elif copy.board[row][col] == 2:
					count2 += 1
					print("Player 2 move at: Row ", row, " Col ", col, " (TRUE INDEXED)")
				else:
					print("blank")#idk wtf

		print("Number of ones: ", ones, " twos: ", twos, " threes: ", threes, "fours: ", fours)
		print(" Here's count 2: ", count2)
		# EXIT BS HERE

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




