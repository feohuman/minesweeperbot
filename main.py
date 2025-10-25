import time
import random
import numpy as np
	
class Minesweeper:
	def __init__(self, height, width):
		# Set minecount to the standard difficulty
		self.width = width
		self.height = height
		self.minecount = round(height * width * 0.15625)
		self.mines = set()

		for mine in range(self.minecount):
			ok = False
			while not ok:
				mineX = random.randint(0, self.height - 1)
				mineY = random.randint(0, self.width - 1)

				if (mineX, mineY) not in self.mines:
					self.mines.add((mineX, mineY))
					ok = True

		self.numbers = np.zeros((height, width))

		self.algnumbers = np.full((height, width), -1, dtype="int")

		for i in range(self.height):
			for j in range(self.width):

				if (i, j) in self.mines:
					self.numbers[i][j] = -1
					continue
				
				number = 0

				for k in range(i-1, i+2):
					for l in range(j-1, j+2):
						if (k, l) in self.mines and k < self.height and l < self.width:
							number += 1

				self.numbers[i][j] = number

		self.unknown = set()
		for i in range(self.height):
			for j in range(self.width):
				self.unknown.add((i, j))

		self.known_safes = set()
		self.known_mines = set()

	def show_info(self):
		print(f"Height = {self.height} ; Width = {self.width}\n")
		for mineX, mineY in self.mines :
			print(f"Mine(X, Y): {mineX}, {mineY}\n")
		print(self.mines.__len__())

	def show_full_board(self):
		board = np.full((self.height , self.width), ' ', dtype='U1')
		for i in range(self.height):
			for j in range(self.width):
				board[i][j] = self.numbers[i][j]
				if (i, j) in self.known_mines:
					board[i][j] = '*'
		print(board)
		print("\n")

	def show_exposed_board(self):
		board = np.full((self.height , self.width), '?', dtype='U1')
		for x, y in self.known_safes:
			if self.numbers[x][y] > 0:
				board[x][y] = self.numbers[x][y]
			else:
				board[x][y] = ' '
		for x, y in self.known_mines:
			board[x][y] = '*'
		print(board)
		print("\n")
	
	def solve(self):
		x = random.randint(0, self.height - 1)
		y = random.randint(0, self.width - 1)
		next_move = set()
		next_move.add((x, y))
		status = True
		while status and (len(self.known_mines) != self.minecount) and (len(self.unknown) != 0):

			time.sleep(0.1)
			move = next_move.pop()

			# input()

			status = self.expose_cell(move[0], move[1])
			self.show_exposed_board()

			if not status:
				break

			change = True

			while change:

				change = False

				for i, j in self.known_safes:
					if self.algnumbers[i][j] == 0:
						continue

					local_possible_count = 0
					local_known_count = 0

					local_possible_mines = set()
					local_known_mines = set()
					
					for k, l in self.neighbors(i, j):
						if (k, l) not in self.known_safes:
							local_possible_count += 1
							local_possible_mines.add((k, l))
					
						if (k, l) in self.known_mines:
							local_known_count += 1
							local_known_mines.add((k, l))

					if self.algnumbers[i][j] == local_possible_count:
						for mx, my in local_possible_mines:
							if (mx, my) not in self.known_mines:
								change = True
								self.known_mines.add((mx, my))
					
					if self.algnumbers[i][j] == local_known_count:
						for mine in local_known_mines:
							local_possible_mines.remove(mine)
						for safe in local_possible_mines:
							next_move.add(safe)
					local_possible_mines.clear()

				self.unknown.difference_update(self.known_mines)
				self.unknown.difference_update(self.known_safes)

				if len(next_move) == 0 and status and (len(self.known_mines) != self.minecount) and (len(self.unknown) != 0):
					next_move.add(self.unknown.pop())

				self.show_exposed_board()
		return status

	def expose_cell(self, x, y):
		if (x, y) in self.mines:
			self.show_full_board()
			return False
		self.flood_fill(x, y)
		return True
		

	def flood_fill(self, x, y):
		queue = []
		visited = set()
		queue.append((x, y))
		while len(queue):
			i, j = queue.pop(0)
			self.known_safes.add((i, j))
			self.algnumbers[i][j] = self.numbers[i][j]
			visited.add((i, j))

			if self.algnumbers[i][j] == 0:
				for k in range(i-1, i+2):
					for l in range(j-1, j+2):
						if (k, l) not in visited and k in range(self.height) and l in range(self.width):
								queue.append((k, l))
			
	def neighbors(self, x, y):
		neighbors = set()
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				if i in range(self.height) and j in range(self.width):
					neighbors.add((i, j))
		neighbors.remove((x, y))
		return neighbors




		
def main():
	x = input("Select Seed:")
	random.seed(x)

	
	x = input("Select Height:")
	y = input("Select Width:")
	game = Minesweeper(int(x), int(y))
	status = game.solve()
	if status:
		print("You win")
		return
	print("You lose")

if __name__ == "__main__":
	main()