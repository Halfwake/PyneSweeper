#PyneSweeper, MineSweeper with wrap around
#Started: 03/12/12
#Updated: 03/13/12
#Finished: ?

import os
import sys
from Tkinter import *
from tkMessageBox import *
from random import choice


def pack_game(parent, gridsize):
    "Pack the 'parent' with a column of frames."
    #Set up empty grid
    gamegrid = [0] * gridsize
    for i in range(len(gamegrid)):
        gamegrid[i] = [0] * gridsize
    #Fill grid with MineSpaces 
    for y in xrange(gridsize):
        iter_frame = Frame(parent) #Call the frame
        iter_frame.pack(side = "top") #And pack it
        for x in range(gridsize):
            iter_mine = MineSpace(iter_frame, x, y) #Call the minespace
            gamegrid[x][y] = iter_mine #Put it in the grid
            iter_mine.pack(side = "left") #And display it
    return gamegrid

def fill_grid(gamegrid):
    "Fills grid with mines and then nums"
    #Fills grid with mines
    for i in range(int((1 - minepercent) * gridsize)):
        row_choice = choice(gamegrid)
        column_choice = choice(row_choice)
        column_choice.mine = 1
    #Change 'self.num' of 'MineSpace's
    for x in range(gridsize):
        for y in range(gridsize):
            gamegrid[x][y].check_num()

def win_check(gridsize, gamegrid):
    #win_check(gridsize, gamegrid)
    "To be run after every click, checks if game is won"
    for x in range(gridsize):
        for y in range(gridsize):
            iter_mine = gamegrid[x][y]
            if not iter_mine.clicked:
                if not iter_mine.mine:
                    return 0
    else:
        game_over(gamegrid)
        
def console_run():
    "Runs the game from console on *nix or windows."
    name = sys.platform
    if name[:3] == "win":
        os.system("start " + sys.argv[0])
    else:
        os.system("python " + sys.argv[0])
        
def game_over(gamegrid):
    "Called on game end"
    for x in range(gridsize):
        for y in range(gridsize):
            iter_mine = gamegrid[x][y]
            if iter_mine.mine:
                iter_mine.config(bg = "black", text = "*", state = "disabled")
    if askyesno("Game Over", "Do you want to start a new game?"):
        root.quit()
        console_run() #Starts a game within the function, probably not the best solution
    else:
        root.quit()

class MineSpace(Button):
    "MineSpace is a class representing a space on a minesweeper board."
    def __init__(self, parent, x, y):
        Button.__init__(self, parent, height = 3, width = 5, bg = "blue")
        self.x = x
        self.y = y
        self.num = 0 #Number of surrounding mines
        self.marked = 0 #Whether it's marked as a mine or not
        self.clicked = 0
        self.mine = 0
        self.bind("<Button-1>", self.click_command)
        self.bind("<Button-3>", self.mark_command)
    def click_command(self, event):
        "Method for a primary mouse button click"
        if not self.marked:
            self.clicked = 1
            if self.mine:
                self.config(bg = "black", text = "*", state = "disabled")
                game_over(gamegrid)
            elif self.num > 0:
                self.config(bg = "grey", fg = "green", text = str(self.num), state = "disabled")
            else:
                self.clear_flood()
        win_check(gridsize, gamegrid)
    def mark_command(self, event):
        "Method for a secondary mouse button click"
        if not self.clicked:
            if self.marked:
                self.marked = 0
                self.config(bg = "blue", text = "", state = "active")
            elif not self.marked:
                self.marked = 1
                self.config(bg = "red", text = "%", state = "disabled")
    def clear_flood(self):
        "Uses floodfill to clear surrounding clear and number tiles, only recurses in clear tiles"
        self.config(bg = "grey", text = "", state = "disabled")
        self.clicked = 1
        for i in range(-1,2):
            for j in range(-1,2):
##                if abs(i) == abs(j): #If it's a diagnal fill skip it
##                    continue
                if i == 0 and j == 0: #If the tile itself skip it
                    continue
                x, y = self.wrap_num(self.x, self.y, i, j) #Wrap num around 'gamegrid' to avoid an 'IndexError'
                iter_mine = gamegrid[x][y] #Local var convanience
                if iter_mine.mine == 0:
                    if iter_mine.num > 0:
                        iter_mine.clicked = 1
                        iter_mine.config(bg = "grey", fg = "green", text = str(iter_mine.num), state = "disabled")
                    elif not iter_mine.clicked:
                        iter_mine.clear_flood()
    def check_num(self):
        "Sets the 'self.num' of a MineSpace to the number of tiles surrounding it"
        total_mine = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                x, y = self.wrap_num(self.x, self.y, i, j)
                if gamegrid[x][y].mine:
                    total_mine += 1
        self.num = total_mine

                
    def wrap_num(self, x, y, i, j):
        "Wraps 'x' and 'y' around so that 'gamegrid' doesn't get an idex error"
        x += i
        y += j
        if x > gridsize - 1:
            x -= gridsize + 1
        if y > gridsize - 1:
            y -= gridsize + 1
        return x, y


root = Tk() #Main app
root.title("PyneSweeper")
root.iconbitmap("pinecone.png")
gridsize = 8 #Length and width of grid
minepercent = 0.1 #Percent of tiles that are mines
gamegrid = pack_game(root, gridsize) #Sets up a grid of 'MineSpace's and packs them
fill_grid(gamegrid) #Fills grid with mines
root.mainloop()
