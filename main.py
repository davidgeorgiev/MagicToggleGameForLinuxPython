from colorama import init
init()
from colorama import Fore, Back, Style
from os import system, name
import sys, time
import random
import copy

import termios, sys, os
TERMIOS = termios
 #Colors for game #C6BEA7,#8C8771,#CF542F,#CC0000,#1D4D95,#350000,#003F07,#C4A000
def getkey():
	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
	new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
	new[6][TERMIOS.VMIN] = 1
	new[6][TERMIOS.VTIME] = 0
	termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
	c = None
	try:
		c = os.read(fd, 1)
	finally:
		termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
	return c
class MagicToggleGame():
	def __init__(self,parent):
		self.boardList = list()
		self.x = 0
		self.y = 0
		self.x_cp = 1
		self.y_cp = 1

		self.lastX = -1
		self.lastY = -1
		self.lastPlayer = 0
		self.gamemode = 1
		self.last_turn_score = 0
		self.fast_or_not = 0
		self.game_level = 2

		self.analysis_finished = 1

	def InitBoard(self):
		x = int(raw_input("enter x size: "))
		y = int(raw_input("enter y size: "))
		self.SetBoard(x,y)
	def SetBoard(self,x,y):
		self.x = x
		self.y = y
		self.boardList = list()
		i = 0
		while (i < self.y):
			i+=1
			listofzeros = [0] * self.x
			self.boardList.append(listofzeros)
		self.boardList[y/2][x/2] = 1
		self.boardList[y/2][x/2-1] = 2
		self.boardList[y/2-1][x/2-1] = 1
		self.boardList[y/2-1][x/2] = 2
		self.x_cp = x/2
		self.y_cp = y/2+2
	def CountObjectsOnBoard(self):
		player1 = 0
		player2 = 0
		for i in self.boardList:
			for k in i:
				if(k==1):
					player1+=1
				if(k==2):
					player2+=1
		return [player1,player2]
	def IfBoardIsFull(self):
		full = 1
		for i in self.boardList:
			for k in i:
				if(k == 0):
					full = 0
		return full
	def ShowBoard(self):
		score = [0,0]
		sys.stdout.write("\033[37m")
		my_curse3 = "\033[01;99m"
		my_curse4 = "\033[01;103m"
		my_curse1 = Back.BLACK
		my_curse0 = "\033[01;100m"
		my_curse00 = "\033[01;47m"
		sys.stdout.write(my_curse3)
		sys.stdout.write(my_curse1)
		#for i in range(255):
		#	sys.stdout.write("\033[30m\033[01;"+str(i)+"m")
		#	sys.stdout.write(str(i)+",")
		print("")
		print("\n\n\n\n\n\n\n\n\n\n\n\n  MAGIC TOGGLE\n")
		if(self.gamemode == 2):
			if(self.game_level==1):
				print("      easy    ")
			if(self.game_level==2):
				print("     normal   ")
			if(self.game_level==3):
				print("      hard    ")
			if(self.game_level==4):
				print("    imposible ")
		else:
			print("   multiplayer")
			
		sys.stdout.write("\033[30m")
		print("")
		
		sys.stdout.write("   ")
		sys.stdout.write(my_curse4)
		for i in range(len(self.boardList)+2):
			sys.stdout.write(" ")
		sys.stdout.write(my_curse1)
		print("")
		c_x = 1
		c_y = 1
		my_bool = 0
		for i in self.boardList:
			sys.stdout.write("   ")
			sys.stdout.write(my_curse4)
			sys.stdout.write(" ")
			sys.stdout.write(my_curse1)
			my_curse2 = ""
			my_bool = not my_bool
			for k in i:
				#print(k),
				if k == 1:
					sys.stdout.write("\033[31m")
				elif k == 2:
					sys.stdout.write("\033[34m")
				else:
					sys.stdout.write("\033[30m")
				if(c_x%2==my_bool):
					my_curse2 = my_curse0
				else:
					my_curse2 = my_curse00
				sys.stdout.write(my_curse2)
				if(c_x == self.x_cp or c_y == self.y_cp):
					sys.stdout.write(my_curse1)
				if(c_x-1 == self.lastX and c_y-1 == self.lastY):
					sys.stdout.write(my_curse4)
				if(k==1):
					sys.stdout.write(unichr(234))#9672 9642 9899
				elif(k==2):
					sys.stdout.write(unichr(212))
				else:
					sys.stdout.write(" ")
				sys.stdout.write(my_curse1)
				c_x += 1
			c_x = 1
			sys.stdout.write(my_curse4)
			sys.stdout.write(" ")
			sys.stdout.write(my_curse1)
			print("")
			c_y += 1
		sys.stdout.write("   ")
		sys.stdout.write(my_curse4)
		for i in range(len(self.boardList)+2):
			sys.stdout.write(" ")
		sys.stdout.write(my_curse1)
		sys.stdout.write("\n")
		sys.stdout.write("\033[37m")
		score = self.CountObjectsOnBoard()
		if(self.IfBoardIsFull() and self.analysis_finished == 1):
			score = self.CountObjectsOnBoard()
			sys.stdout.write("\n")
			if(score[0]>score[1]):
				sys.stdout.write("\033[31m"+"   Red wins!"+"\033[37m\n")
			if(score[0]<score[1]):
				sys.stdout.write("\033[34m"+"   Blue wins!"+"\033[37m\n")
			if(score[0]==score[1]):
				sys.stdout.write(my_curse3+"   Both wins!"+"\033[37m\n")
		#print(self.GetAllAvailablePositions())
		#print("last turn score is "+str(self.last_turn_score))
		score = self.CountObjectsOnBoard()
		sys.stdout.write("\n\033[31m"+"   "+unichr(234)+": "+str(score[0])+" "+"\033[34m"+unichr(212)+": "+str(score[1])+"\033[37m\n")
		#sys.stdout.write("\nquit by pressing ctrl + c")
	def SetCurrentPos(self,player_num):
		return self.SetPos(player_num,self.x_cp,self.y_cp)
	def SetPos(self,player_num,x_cp,y_cp):
		#print("setting position")
		k = 0
		i = 0
		#print(self.y)
		while(k < self.y):
			#print("k = "+str(k))
			while(i < self.x):
				#print(str(i)+" "+str(k))
				if(i == x_cp-1 and k == y_cp-1):
					if(self.CheckIfPosIsValid(x_cp,y_cp)):
						self.boardList[k][i] = player_num
						self.lastPlayer = player_num
						self.lastX = i
						self.lastY = k
						self.x_cp = i+1
						self.y_cp = k+1
						self.LastTurnSearchAndChange(player_num)
					else:
						return 0
					#print("done")
				i+=1
			i=0
			k+=1
		return 1
	def DoRandomTurn(self,player_num):
		my_list = self.GetAllAvailablePositions()
		rand_choice = random.choice(my_list)
		self.SetPos(player_num,rand_choice[0],rand_choice[1])
		#print(player_num,rand_choice[0],rand_choice[1])
	def DoSmartTurn(self,player_num):
		list_pos_and_score = list()
		my_list = self.GetAllAvailablePositions()
		if(len(my_list)==0):
			return 0
		random.shuffle(my_list)
		last_board_state = copy.deepcopy(self.boardList)
		max_score = 0
		best_pos_index = 0
		i = 0
		for pos in my_list:
			self.fast_or_not = 1
			self.SetPos(player_num,pos[0],pos[1])
			if(self.last_turn_score > max_score):
				best_pos_index = i
				max_score = self.last_turn_score
			i+=1
			list_pos_and_score.append([pos[0],pos[1],self.last_turn_score])
			self.boardList = copy.deepcopy(last_board_state)
			#self.ShowBoard()

		list_pos_and_score.sort(key=lambda x: x[2])
		#for i in list_pos_and_score:
		#	print(i)
		#string = raw_input("Enter new Note ")
		#for info in list_pos_and_score:
			#print(info)
		#print("Best pos: "),
		#print([my_list[best_pos_index][0],my_list[best_pos_index][1],max_score])
		#string = raw_input("Enter new Note ")
		self.fast_or_not = 0
		chance_list = [0, 0, 1]
		random.shuffle(chance_list)
		j = -1
		try:
			while(list_pos_and_score[j][2]==list_pos_and_score[j-1][2]):
				j-=1
		except:
			j = 1
		if(self.game_level == 1):
			if(chance_list[0]==0):
				self.SetPos(player_num,list_pos_and_score[0][0],list_pos_and_score[0][1])
			else:
				self.SetPos(player_num,list_pos_and_score[j-1][0],list_pos_and_score[j-1][1])
		if(self.game_level == 2):
			if(chance_list[0]==0):
				self.SetPos(player_num,list_pos_and_score[j-1][0],list_pos_and_score[j-1][1])
			else:
				self.SetPos(player_num,list_pos_and_score[-1][0],list_pos_and_score[-1][1])
			#print(list_pos_and_score[j-1])
			#string = raw_input("Enter new Note ")
		if(self.game_level == 3):
			if(chance_list[0]==0):
				self.SetPos(player_num,list_pos_and_score[-1][0],list_pos_and_score[-1][1])
			else:
				self.SetPos(player_num,list_pos_and_score[j-1][0],list_pos_and_score[j-1][1])
		if(self.game_level == 4):
			self.SetPos(player_num,list_pos_and_score[-1][0],list_pos_and_score[-1][1])
		#print(max_score)
		#print(player_num,my_list[best_pos_index][0],my_list[best_pos_index][1])
		#string = raw_input("Enter new Note ")

		#print(player_num,rand_choice[0],rand_choice[1])
	def GetAllAvailablePositions(self):
		all_available_positions = list()
		#print("setting position")
		k = 0
		i = 0
		#print(self.y)
		while(k <= self.y):
			#print("k = "+str(k))
			while(i <= self.x):
				if(self.CheckIfPosIsValid(i,k)==1):
					all_available_positions.append([i,k])
				i+=1
			i=0
			k+=1
		return all_available_positions
	def CheckIfCurrentPosIsValid(self):
		return self.CheckIfPosIsValid(self.x_cp,self.y_cp)
	def CheckIfPosIsValid(self,x_cp,y_cp):
		#print("setting position")
		k = 0
		i = 0
		flag = 0
		#print(self.y)
		while(k < self.y):
			#print("k = "+str(k))
			while(i < self.x):
				
				if(i == x_cp-1 and k == y_cp-1):
					
					if(self.boardList[k][i] != 0):
						return 0
					k_up = k
					k_down = k
					i_up = i
					i_down = i
					#print(self.boardList[k][i])
					#print([k_up,k_down,i_up,i_down])
					if(k+1 < self.y):
						k_up = k+1
					if(k-1 >= 0):
						k_down = k-1
					if(i+1 < self.x):
						i_up = i+1
					if(i-1 >= 0):
						i_down = i-1
					#print([k_up,k_down,i_up,i_down])
					if(self.boardList[k_down][i] != 0):
						flag = 1
						#print(k_down,i)
					if(self.boardList[k_up][i] != 0):
						flag = 1
						#print(k_up,i)
					if(self.boardList[k][i_down] != 0):
						flag = 1
						#print(k,i_down)
					if(self.boardList[k][i_up] != 0):
						flag = 1
						#print(k,i_up)
					if(self.boardList[k_up][i_up] != 0):
						flag = 1
						#print(k_up,i_up)
					if(self.boardList[k_down][i_up] != 0):
						flag = 1
						#print(k_down,i_up)
					if(self.boardList[k_down][i_down] != 0):
						flag = 1
						#print(k_down,i_down)
					if(self.boardList[k_up][i_down] != 0):
						flag = 1
						#print(k_up,i_down)
					return flag
					
					#print("done")
				i+=1
			i=0
			k+=1
	def LastTurnSearchAndChange(self,p_n):
		self.analysis_finished = 0
		turn_score = 0
		x = self.lastX
		y = self.lastY
		my_player_num = p_n
		#searching in right way
		inc_val = 1
		change_flag = 0
		end_flag = 0

		while True:
			if(x+inc_val<self.x):
				x+=inc_val
			else:
				end_flag = 1
			if(change_flag == 1):
				if(self.boardList[y][x]!=my_player_num):
					turn_score+=1
					if(self.fast_or_not==0):
						time.sleep(.300)
					self.boardList[y][x] = my_player_num
					if(self.fast_or_not==0):
						self.ShowBoard()
						time.sleep(.300)
			if(self.boardList[y][x]==my_player_num or self.boardList[y][x]==0 or end_flag == 1):
				inc_val = -1
			if(self.boardList[y][x]==my_player_num):
				change_flag = 1
			if(x==self.lastX and y==self.lastY):
				break
		#searching in left way
		inc_val = -1
		change_flag = 0
		end_flag = 0
		x = self.lastX
		y = self.lastY
		while True:
			if(x+inc_val>=0):
				x+=inc_val
			else:
				end_flag = 1
			if(change_flag == 1):
				if(self.boardList[y][x]!=my_player_num):
					turn_score+=1
					if(self.fast_or_not==0):
						time.sleep(.300)
					self.boardList[y][x] = my_player_num
					if(self.fast_or_not==0):
						self.ShowBoard()
						time.sleep(.300)
			if(self.boardList[y][x]==my_player_num or self.boardList[y][x]==0 or end_flag == 1):
				inc_val = 1
			if(self.boardList[y][x]==my_player_num):
				change_flag = 1
			if(x==self.lastX and y==self.lastY):
				break
		#searching in up way
		inc_val = -1
		change_flag = 0
		end_flag = 0
		x = self.lastX
		y = self.lastY
		while True:
			if(y+inc_val>-1):
				y+=inc_val
			else:
				end_flag = 1
			if(change_flag == 1):
				if(self.boardList[y][x]!=my_player_num):
					turn_score+=1
					if(self.fast_or_not==0):
						time.sleep(.300)
					self.boardList[y][x] = my_player_num
					if(self.fast_or_not==0):
						self.ShowBoard()
						time.sleep(.300)
			if(self.boardList[y][x]==my_player_num or self.boardList[y][x]==0 or end_flag == 1):
				inc_val = 1
			if(self.boardList[y][x]==my_player_num):
				change_flag = 1
			if(x==self.lastX and y==self.lastY):
				break
		#searching in down way
		inc_val = 1
		change_flag = 0
		end_flag = 0
		x = self.lastX
		y = self.lastY
		while True:
			if(y+inc_val<self.y):
				y+=inc_val
			else:
				end_flag = 1
			if(change_flag == 1):
				if(self.boardList[y][x]!=my_player_num):
					turn_score+=1
					if(self.fast_or_not==0):
						time.sleep(.300)
					self.boardList[y][x] = my_player_num
					if(self.fast_or_not==0):
						self.ShowBoard()
						time.sleep(.300)
			if(self.boardList[y][x]==my_player_num or self.boardList[y][x]==0 or end_flag == 1):
				inc_val = -1
			if(self.boardList[y][x]==my_player_num):
				change_flag = 1
			if(x==self.lastX and y==self.lastY):
				break

		#searching in up-right way
		inc_val = 1
		change_flag = 0
		end_flag = 0
		x = self.lastX
		y = self.lastY
		while True:
			if(y-inc_val>-1 and x+inc_val<self.x):
				y-=inc_val
				x+=inc_val
			else:
				end_flag = 1
			if(change_flag == 1):
				if(self.boardList[y][x]!=my_player_num):
					turn_score+=1
					if(self.fast_or_not==0):
						time.sleep(.300)
					self.boardList[y][x] = my_player_num
					if(self.fast_or_not==0):
						self.ShowBoard()
						time.sleep(.300)
			if(self.boardList[y][x]==my_player_num or self.boardList[y][x]==0 or end_flag == 1):
				#print("changed")
				inc_val = -1
			if(self.boardList[y][x]==my_player_num):
				change_flag = 1
			if(x==self.lastX and y==self.lastY):
				break
		#searching in down-right way
		inc_val = 1
		change_flag = 0
		end_flag = 0
		x = self.lastX
		y = self.lastY
		while True:
			if(y+inc_val<self.y and x+inc_val<self.x):
				y+=inc_val
				x+=inc_val
			else:
				end_flag = 1
			if(change_flag == 1):
				if(self.boardList[y][x]!=my_player_num):
					turn_score+=1
					if(self.fast_or_not==0):
						time.sleep(.300)
					self.boardList[y][x] = my_player_num
					if(self.fast_or_not==0):
						self.ShowBoard()
						time.sleep(.300)
			if(self.boardList[y][x]==my_player_num or self.boardList[y][x]==0 or end_flag == 1):
				#print("changed")
				inc_val = -1
			if(self.boardList[y][x]==my_player_num):
				change_flag = 1
			if(x==self.lastX and y==self.lastY):
				break
		#searching in up-left way
		inc_val = 1
		change_flag = 0
		end_flag = 0
		x = self.lastX
		y = self.lastY
		while True:
			if(y-inc_val>-1 and x-inc_val>=0):
				y-=inc_val
				x-=inc_val
			else:
				end_flag = 1
			if(change_flag == 1):
				if(self.boardList[y][x]!=my_player_num):
					turn_score+=1
					if(self.fast_or_not==0):
						time.sleep(.300)
					self.boardList[y][x] = my_player_num
					if(self.fast_or_not==0):
						self.ShowBoard()
						time.sleep(.300)
			if(self.boardList[y][x]==my_player_num or self.boardList[y][x]==0 or end_flag == 1):
				#print("changed")
				inc_val = -1
			if(self.boardList[y][x]==my_player_num):
				change_flag = 1
			if(x==self.lastX and y==self.lastY):
				break
		#searching in down-left way
		inc_val = 1
		change_flag = 0
		end_flag = 0
		x = self.lastX
		y = self.lastY
		while True:
			if(y+inc_val<self.y and x-inc_val>=0):
				y+=inc_val
				x-=inc_val
			else:
				end_flag = 1
			if(change_flag == 1):
				if(self.boardList[y][x]!=my_player_num):
					turn_score+=1
					if(self.fast_or_not==0):
						time.sleep(.300)
					self.boardList[y][x] = my_player_num
					if(self.fast_or_not==0):
						self.ShowBoard()
						time.sleep(.300)
			if(self.boardList[y][x]==my_player_num or self.boardList[y][x]==0 or end_flag == 1):
				#print("changed")
				inc_val = -1
			if(self.boardList[y][x]==my_player_num):
				change_flag = 1
			if(x==self.lastX and y==self.lastY):
				break
		self.last_turn_score = turn_score
		self.analysis_finished = 1

	def IncCurX(self):
		if(self.x_cp<self.x):
			self.x_cp+=1
	def IncCurY(self):
		if(self.y_cp<self.y):
			self.y_cp+=1
	def DecCurX(self):
		if(self.x_cp>1):
			self.x_cp-=1
	def DecCurY(self):
		if(self.y_cp>1):
			self.y_cp-=1

class GameMenu():
	def __init__(self,parent):
		self.parent = parent
		self.list_of_modes = [" MULTIPLAYER ","     CPU     "]
		self.list_of_players = ["\033[31m    FIRE     \033[37m","\033[34m    WATER    \033[37m"]
		self.list_of_sizes = ["      04     ","      06     ","      08     ","      10     ","      12     ","      14     ","      16     "]
		self.list_of_levels = ["     EASY    ","    NORMAL   ","     HARD    ","  IMPOSIBLE  "]
		self.current_index = 0

		self.my_curse5 = "\033[37m"
		self.my_curse3 = "\033[01;99m"
		self.my_curse4 = "\033[01;103m"
		self.my_curse1 = Back.BLACK
		self.my_curse0 = "\033[01;100m"
		self.my_curse00 = "\033[01;47m"
		self.my_curse6 = "\033[105m"

	def IncIndex(self,max_index):
		if(self.current_index+1<=max_index):
			self.current_index+=1
	def DecIndex(self):
		if(self.current_index-1>=0):
			self.current_index-=1

	def ShowModeMenu(self,title1,title2):
		
		sys.stdout.write(self.my_curse1)
		sys.stdout.write(self.my_curse3)
		sys.stdout.write("\033[37m")
		self.current_index = 0
		first_time = 1
		key = ""
		while True:
			if(first_time == 0):
				key = str(getkey())
			else:
				first_time = 0
			if key == "8":
				#print("Move up")
				self.DecIndex()
				first_time = 0
			if key == "5":
				#print("Move down")
				
				self.IncIndex(len(self.list_of_modes)-1)
			sys.stdout.write(title1+"\n"+title2+"\n")
			i = 0
			sys.stdout.write(" ")
			sys.stdout.write(self.my_curse4)
			sys.stdout.write("               ")
			sys.stdout.write(self.my_curse1)
			sys.stdout.write("\n")
			for item in self.list_of_modes:
				sys.stdout.write(" ")
				sys.stdout.write(self.my_curse4)
				sys.stdout.write(" ")
				sys.stdout.write(self.my_curse1)
				if(i == self.current_index):
					sys.stdout.write(self.my_curse6)
				sys.stdout.write(item)
				i+=1
				sys.stdout.write(self.my_curse4)
				sys.stdout.write(" ")
				sys.stdout.write(self.my_curse1)
				sys.stdout.write("\n")
			sys.stdout.write(" ")
			sys.stdout.write(self.my_curse4)
			sys.stdout.write("               ")
			sys.stdout.write(self.my_curse1)
			sys.stdout.write("\n")
			if key == "\n":
				break
			sys.stdout.write("\n\n\n\n\n")
		return self.current_index+1
	def ShowSelectPlayer(self,title1,title2):
		
		sys.stdout.write(self.my_curse1)
		sys.stdout.write(self.my_curse3)
		sys.stdout.write("\033[37m")
		self.current_index = 0
		first_time = 1
		key = ""
		while True:
			if(first_time == 0):
				key = str(getkey())
			else:
				first_time = 0
			if key == "8":
				#print("Move up")
				self.DecIndex()
				first_time = 0
			if key == "5":
				#print("Move down")
				
				self.IncIndex(len(self.list_of_players)-1)
			sys.stdout.write(title1+"\n"+title2+"\n")
			i = 0
			sys.stdout.write(" ")
			sys.stdout.write(self.my_curse4)
			sys.stdout.write("               ")
			sys.stdout.write(self.my_curse1)
			sys.stdout.write("\n")
			for item in self.list_of_players:
				sys.stdout.write(" ")
				sys.stdout.write(self.my_curse4)
				sys.stdout.write(" ")
				sys.stdout.write(self.my_curse1)
				if(i == self.current_index):
					sys.stdout.write(self.my_curse6)
				sys.stdout.write(item)
				i+=1
				sys.stdout.write(self.my_curse4)
				sys.stdout.write(" ")
				sys.stdout.write(self.my_curse1)
				sys.stdout.write("\n")
			sys.stdout.write(" ")
			sys.stdout.write(self.my_curse4)
			sys.stdout.write("               ")
			sys.stdout.write(self.my_curse1)
			sys.stdout.write("\n")
			if key == "\n":
				break
			sys.stdout.write("\n\n\n\n\n")
		return self.current_index+1

	def ShowSizeMenu(self,title1,title2):
		sys.stdout.write(self.my_curse1)
		sys.stdout.write(self.my_curse3)
		sys.stdout.write("\033[37m")
		self.current_index = 0
		first_time = 1
		key = ""
		while True:
			if(first_time == 0):
				key = str(getkey())
			else:
				first_time = 0
			if key == "8":
				#print("Move up")
				self.DecIndex()
			if key == "5":
				#print("Move down")
				self.IncIndex(len(self.list_of_sizes)-1)

			sys.stdout.write(title1+"\n"+title2+"\n")
			
			sys.stdout.write(" ")
			sys.stdout.write(self.my_curse4)
			sys.stdout.write("               ")
			sys.stdout.write(self.my_curse1)
			sys.stdout.write("\n")

			sys.stdout.write(" ")
			sys.stdout.write(self.my_curse4)
			sys.stdout.write(" ")
			sys.stdout.write(self.my_curse1)
			sys.stdout.write(self.my_curse6)
			sys.stdout.write(self.list_of_sizes[self.current_index])
			sys.stdout.write(self.my_curse4)
			sys.stdout.write(" ")
			sys.stdout.write(self.my_curse1)
			sys.stdout.write("\n")

			sys.stdout.write(" ")
			sys.stdout.write(self.my_curse4)
			sys.stdout.write("               ")
			sys.stdout.write(self.my_curse1)
			sys.stdout.write("\n")
			if key == "\n":
				break
			sys.stdout.write("\n\n\n\n\n\n")
		return self.list_of_sizes[self.current_index]
	def ShowLevelsMenu(self,title1,title2):
		sys.stdout.write(self.my_curse1)
		sys.stdout.write(self.my_curse3)
		sys.stdout.write("\033[37m")
		self.current_index = 0
		first_time = 1
		key = ""
		while True:
			if(first_time == 0):
				key = str(getkey())
			else:
				first_time = 0
			if key == "8":
				#print("Move up")
				self.DecIndex()
			if key == "5":
				#print("Move down")
				
				self.IncIndex(len(self.list_of_levels)-1)
			sys.stdout.write(title1+"\n"+title2+"\n")
			i = 0
			sys.stdout.write(" ")
			sys.stdout.write(self.my_curse4)
			sys.stdout.write("               ")
			sys.stdout.write(self.my_curse1)
			sys.stdout.write("\n")
			for item in self.list_of_levels:
				sys.stdout.write(" ")
				sys.stdout.write(self.my_curse4)
				sys.stdout.write(" ")
				sys.stdout.write(self.my_curse1)
				if(i == self.current_index):
					sys.stdout.write(self.my_curse6)
				
				sys.stdout.write(item)
				sys.stdout.write(self.my_curse4)
				sys.stdout.write(" ")
				sys.stdout.write(self.my_curse1)
				i+=1
				sys.stdout.write("\n")
			if key == "\n":
				break
			sys.stdout.write(" ")
			sys.stdout.write(self.my_curse4)
			sys.stdout.write("               ")
			sys.stdout.write(self.my_curse1)
			sys.stdout.write("\n\n\n\n")
		return self.current_index+1

if __name__ == "__main__":
	'''k = 0
	for i in range(100000):
		if(k%100 == 1):
			key = str(getkey())
		print(str(i)+": "),
		print(unichr(i))
		k+=1
	'''
	

	#MyMagicToggleGame.InitBoard()
	'''while(1):
		y_size = raw_input("enter y size of the game field - min:8, max:16 - ")
		x_size = raw_input("enter x size of the game field - min:8, max:16 - ")
		try:
			if(int(x_size) <=16 and int(y_size) <=16 and int(x_size) >=8 and int(y_size) >=8):
				MyMagicToggleGame.SetBoard(int(x_size),int(y_size))
				break
		except:
			a=0
	while(1):
		difficulty = int(raw_input("enter difficulty (a digit from 1 to 4): "))
		try:
			if(difficulty>=1 and difficulty<=4):
				MyMagicToggleGame.game_level = difficulty
				break
		except:
			a=0
	
	print("\n  Game just started,\n\n controls: numpad(8,5,4,6) and \"enter\" button\n\n I hope you will enjoy!")
	MyMagicToggleGame.gamemode = 2
	'''

	first_time = 0
	player_switcher = 0
	first_time = 1
	key = "8"
	chosen_to_be_first = 1
	while True:
		if(first_time == 0):
				key = str(getkey())
		else:
			MyGameMenu = GameMenu(None)
			MyMagicToggleGame = MagicToggleGame(None)
			board_size = int(MyGameMenu.ShowSizeMenu("\n\n\n\n\n\n\n\n\n\n\n\n  MAGIC TOGGLE","\n  select size\n\n"))
			MyMagicToggleGame.SetBoard(board_size,board_size)
			MyMagicToggleGame.gamemode = int(MyGameMenu.ShowModeMenu("\n\n\n\n\n\n\n\n\n\n\n\n  MAGIC TOGGLE","\n  select mode\n\n"))
			if(MyMagicToggleGame.gamemode == 2):
				MyMagicToggleGame.game_level = int(MyGameMenu.ShowLevelsMenu("\n\n\n\n\n\n\n\n\n\n\n\n  MAGIC TOGGLE","\n  select level\n\n"))
				chosen_to_be_first = 1+int(MyGameMenu.ShowSelectPlayer("\n\n\n\n\n\n\n\n\n\n\n\n  MAGIC TOGGLE","\n  select mode\n\n"))
			first_time = 0
			player_switcher = 0
			key = "8"
			if_succsessfuly_put = 1
			if(MyMagicToggleGame.gamemode == 2):
				player_switcher = not chosen_to_be_first%2
				if(player_switcher == 0):
					MyMagicToggleGame.DoSmartTurn(1)
					MyMagicToggleGame.ShowBoard()
					key = "1"
		if key == "8":
			#print("Move up")
			MyMagicToggleGame.DecCurY()
			MyMagicToggleGame.ShowBoard()
		if key == "5":
			#print("Move down")
			MyMagicToggleGame.IncCurY()
			MyMagicToggleGame.ShowBoard()
		if key == "4":
			#print("Move left")
			MyMagicToggleGame.DecCurX()
			MyMagicToggleGame.ShowBoard()
		if key == "6":
			#print("Move right")
			MyMagicToggleGame.IncCurX()
			MyMagicToggleGame.ShowBoard()
		if key == "0":
			first_time = 1
		if key == "\n":
			if(MyMagicToggleGame.gamemode == 1 and if_succsessfuly_put == 1):
				player_switcher = not player_switcher
			if(player_switcher == 1):
				if(MyMagicToggleGame.SetCurrentPos(1)==1):
					if(MyMagicToggleGame.gamemode == 2):
						MyMagicToggleGame.DoSmartTurn(2)
					MyMagicToggleGame.ShowBoard()
					if_succsessfuly_put = 1
				else:
					if_succsessfuly_put = 0
			if(player_switcher == 0):
				if(MyMagicToggleGame.SetCurrentPos(2)==1):
					if(MyMagicToggleGame.gamemode == 2):
						MyMagicToggleGame.DoSmartTurn(1)
					MyMagicToggleGame.ShowBoard()
					if_succsessfuly_put = 1
				else:
					if_succsessfuly_put = 0
