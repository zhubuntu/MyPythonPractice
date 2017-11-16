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
                if self.filed[i][j]==2048:
                    self.state='Win'
                    return
        if hasBlank:
            self.state='Run'
        else:
            self.state='Lose'

    def run(self,userInput,screen):
        if userInput=='Up':
            pass
        if userInput == 'Down':
            pass
        if userInput == 'Left':
            pass
        if userInput == 'Right':
            pass
        if userInput=='Quit':
            return 'Lose'
        if userInput=='Reset':
            self.reset()
        self.updateState()
        self.draw(screen)
        return self.state

    def draw(self,screen):
        screen.clear()
        def cast(string):
            screen.addstr(string)
        cast('-'*16+'\n')
        for i in range(4):
            for j in range(4):
                cast('|')
                if self.filed[i][j]!=0:
                    cast(' {} '.format(self.filed[i][j]))
                else:
                    cast(' '*3)
            cast('|'+'\n')
            cast('-' * 16+'\n')

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