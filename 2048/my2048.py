# coding: utf-8
import curses
from random import randrange, choice
from collections import defaultdict
actions = ['Up', 'Left', 'Down', 'Right', 'Reset', 'Quit']
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actionsDict = dict(zip(letter_codes, actions * 2))
class Game(object):
    def __init__(self):
        self.reset()
        self.state='Run'

    def genNewNum(self):
        newNum=4 if randrange(100) > 89 else 2
        (i,j)=choice([(i,j) for i in range(4) for j in range(4) if(self.filed[i][j]==0)] )
        self.filed[i][j]=newNum

    def reset(self):
        self.filed = [[0 for i in range(4)] for j in range(4)]
        self.genNewNum()
        self.genNewNum()
    def updateState(self):
        hasBlank=False
        for i in range(4):
            for j in range(4):
                if self.filed[i][j]==0:
                    hasBlank=True
                elif self.filed[i][j]==2048:
                    self.state='Win'
                    return
        if hasBlank:
            self.state='Run'
        else:
            i=1
            while i<4:
                j=1
                while j<4:
                    if (self.filed[i][j]==self.filed[i-1][j])or(self.filed[i][j]==self.filed[i][j-1]):
                        self.state='Run'
                        return
                    j=j+1
                i=i+1
            self.state='Lose'

    def run(self,userInput,screen):
        if userInput=='Up':
            self.moveUp()
        elif userInput == 'Down':
            self.moveDown()
        elif userInput == 'Left':
            self.moveLeft()
        elif userInput == 'Right':
            self.moveRight()
        elif userInput=='Quit':
            return 'Lose'
        elif userInput=='Reset':
            self.reset()
        self.draw(screen)
        self.updateState()  #这里会有一个误判，要注意修改
        return self.state
    def moveUp(self):
        hasChanged=False
        for i in range(4):
            num=[]
            firstZero=4
            for j in range(4):
                if self.filed[j][i]!=0:
                    if(j>firstZero):
                        hasChanged=True
                    num.append(self.filed[j][i])
                else:
                    firstZero=j
            k=len(num) #python list没有size
            for j in range(k-1):
                if num[j]==num[j+1]:
                    hasChanged = True
                    num[j]=num[j]*2
                    num[j+1]=0
            j=0
            for Sinnum in num:
                if Sinnum!=0:
                    self.filed[j][i]=Sinnum
                    j=j+1
            while j<4:
                self.filed[j][i]=0
                j=j+1
        if hasChanged:
            self.genNewNum()
    def moveLeft(self):
        hasChanged = False
        for i in range(4):
            num=[]
            firstZero = 4
            for j in range(4):
                if self.filed[i][j]!=0:
                    if (j > firstZero):
                        hasChanged = True
                    num.append(self.filed[i][j])
                else:
                    firstZero=0
            k = len(num)
            for j in range(k-1):
                if num[j]==num[j+1]:
                    hasChanged = True
                    num[j]=num[j]*2
                    num[j+1]=0
            j=0
            for Sinnum in num:
                if Sinnum!=0:
                    self.filed[i][j]=Sinnum
                    j=j+1
            while j<4:
                self.filed[i][j]=0
                j=j+1
        if hasChanged:
            self.genNewNum()
    def moveRight(self):
        hasChanged = False
        for i in range(4):
            num=[]
            firstNonZero=4
            for j in range(4):
                if self.filed[i][j]!=0:
                    num.append(self.filed[i][j])
                    firstNonZero=j
                else:
                    if firstNonZero<j:
                        hasChanged=True
            num.reverse()
            k = len(num)
            for j in range(k-1):
                if num[j]==num[j+1]:
                    hasChanged=True
                    num[j]=num[j]*2
                    num[j+1]=0
            j=3
            for Sinnum in num:
                if Sinnum!=0:
                    self.filed[i][j]=Sinnum
                    j=j-1
            while(j>=0):
                self.filed[i][j] = 0
                j=j-1
        if hasChanged:
            self.genNewNum()
    def moveDown(self):
        hasChanged=False
        for i in range(4):
            num=[]
            firstNonZero = 4
            for j in range(4):
                if self.filed[j][i]!=0:
                    num.append(self.filed[j][i])
                    firstNonZero=j
                else:
                    if firstNonZero<j:
                        hasChanged=True
            num.reverse()
            k = len(num)
            for j in range(k-1):
                if num[j]==num[j+1]:
                    hasChanged=True
                    num[j]=num[j]*2
                    num[j+1]=0
            j=3
            for Sinnum in num:
                if Sinnum!=0:
                    self.filed[j][i]=Sinnum
                    j=j-1
            while (j >= 0):
                self.filed[j][i] = 0
                j=j-1
        if hasChanged:
            self.genNewNum()
    def draw(self,screen):
        screen.clear()
        def cast(string):
            screen.addstr(string)
        cast('-'*25+'\n')
        for i in range(4):
            for j in range(4):
                cast('|')
                if self.filed[i][j]!=0:
                    cast('{:^5}'.format(self.filed[i][j]))#控制格式化字符长度
                else:
                    cast(' '*5)
            cast('|'+'\n')
            cast('-' * 25+'\n')

def get_user_action(keyboard):
    char = "N"
    while char not in actionsDict:
        char = keyboard.getch()
    return actionsDict[char]
def main(stdscr):
    game=Game()
    state='Init'
    game.draw(stdscr)
    while state!='Win':
        if state=='Lose':
            return
        userInput=get_user_action(stdscr)
        state=game.run(userInput,stdscr)
    return

curses.wrapper(main)