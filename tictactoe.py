# -*- coding: utf-8 -*-
#stab at tic tac toe 
import random
import copy
import logging
from os.path import realpath, join, dirname

log_file = realpath(join(dirname(__file__), "tictactoe.log"))
logging.basicConfig(filename=log_file, filemode="w+", level=logging.DEBUG)
log = logging.getLogger(__name__)

class Board (object):                                   
    def __init__(self, board=None, size=None):
        if board is None:
            if size is None:
                self.size = 3
            else:
                self.size = size
            self.player0_moves = []                             
            self.player1_moves = []
            self.turn = 0     #using this to switch turns 
            self.winner = None
            self.draw = False
        else:
            self.player0_moves = copy.deepcopy(board.player0_moves) 
            self.player1_moves = copy.deepcopy(board.player1_moves)
            self.turn  = board.turn 
            self.size = board.size
            self.winner = board.winner 
            self.draw = board.draw 
    @property
    def BOARD (self):
        BOARD = [[' ']* self.size for x in range(0, self.size) ]
        for (row, col) in self.player0_moves: #(row col is a tuple)
            BOARD[row][col] = 'x'
        for row, col in self.player1_moves:
            BOARD[row][col] = 'o'
        return BOARD
    def show(self):
        for element in self.BOARD:
            print "|"+"|".join(element)+"|"
    @property
    def check_ending ( self ):   
        if check_winning ( self.player0_moves, self.winning_boards ):
           self.winner = "human"
           return True
        elif check_winning ( self.player1_moves, self.winning_boards):
           self.winner = "computer"
           return True
        else:
            for element in self.BOARD:
               for cell in element:
                   if cell == ' ':
                      return False
            self.draw = True
            return True
    @property
    def leaf_value ( self ):                                 
         if self.winner == "human":   
            return -1
         elif self.winner == "computer":
            return 1
         elif self.draw == True:
            return 0
         else:
            print "this is not a terminal board"
    def get_unique_list (self,  a_list ):
        unique_list = []
        for element in a_list:
            if element not in unique_list:
               unique_list.append (element)
        return unique_list
    def get_winning_boards (self):
        #computes the triples of winning positions of any size board
        winning = []
        for x in range(0, self.size):
            for y in range(0, self.size):
                if x - 2 >= 0:
                   winning.append([[x-2,y], [x-1,y], [x,y]])
                if x - 1 >= 0 and x + 1 < self.size:
                   winning.append([[x-1,y], [x,y], [x+1,y]])
                if x + 2 < self.size:
                   winning.append([[x,y],[x+1,y],[x+2,y]])
                if y - 2 >= 0:
                   winning.append([[x,y-2],[x,y-1],[x,y]])
                if y - 1 >= 0 and y + 1 < self.size:
                   winning.append([[x,y-1],[x,y],[x,y+1]])
                if y + 2 < self.size:
                   winning.append([[x,y],[x,y+1],[x,y+2]])
                if x - 1 >= 0 and y - 1>=0 and x + 1 < self.size and y + 1 < self.size:
                   winning.append([[x-1,y-1],[x,y], [x+1,y+1]])
                   winning.append([[x-1,y+1],[x,y],[x+1,y-1]])
        return self.get_unique_list(winning)
#        return set(winning)
      #  return set(winning)
    @property
    def winning_boards (self):
        return self.get_winning_boards()

def play ( a_board, first_player, second_player ):  
        next_turn = Board ( a_board )
        if a_board.turn == 0:
            if first_player == "human":
               next_turn = human_move_result( a_board, human_move( a_board ))
               next_turn.turn = 1 
            elif first_player == "computer":
               next_turn = computer_move ( a_board)
               next_turn.turn = 1 
        elif a_board.turn == 1:
            if second_player == "human":
               next_turn = human_move_result( a_board, human_move( a_board ))
               next_turn.turn = 0 
            elif second_player == "computer":
               next_turn = computer_move ( a_board)
               next_turn.turn = 0 
        return next_turn

def human_move ( a_board ):
    print "place your move. enter row number of move 0 to {size}".format(size=a_board.size)
    row = int(raw_input())               
    print "enter column number of move 0 to {size}".format(size=a_board.size)
    col = int(raw_input())                            #remember to convert to int
    return (row, col)

def computer_move ( a_board ):
    print "player ", a_board.turn, "'s turn"
    return minimax ( a_board, 0 )

def human_move_result ( a_board, the_move ):
    if check_valid_move(a_board, the_move[0], the_move[1]) :
       print "player ", a_board.turn, "'s turn"
       new_board = update_board(a_board, the_move[0], the_move[1])
    else:
       new_board =  human_move_result( a_board, human_move())
    return new_board

def update_board ( a_board, row, col ):   
    a_board = Board(a_board)
    if a_board.turn == 0:
       a_board.player0_moves.append([row, col])
       a_board.BOARD[row][col] = 'x'
       if check_winning(a_board.player0_moves, a_board.winning_boards):
          a_board.winner = "player 0 "
    elif a_board.turn == 1:
        a_board.player1_moves.append([row, col])
        a_board.BOARD[row][col] = 'o'
        if check_winning(a_board.player1_moves, a_board.winning_boards):
          a_board.winner = "player 1"
    else:
        raise Exception("Bad paramater in update_board: player")
    return a_board   
    
def check_winning ( list_of_moves, list_of_winning_boards ):
    for element in list_of_winning_boards:     
        if element[0] in list_of_moves and\
           element[1] in list_of_moves and\
           element[2] in list_of_moves:
           return True
    return False

def check_valid_move ( a_board, row, col ):
   if row > a_board.size or row < 0 or col > a_board.size or col < 0:
        print "invalid move. enter a number between 0 and 2"
        return False
   elif a_board.BOARD[row][col] == ' ':
        return True
   else:
        print "that cell is taken. "    
        return False

def minimax ( a_board, depth ):
    board_temp = Board(a_board)
    if board_temp.check_ending:
       return  board_temp.leaf_value
    if board_temp.turn == 1:
       value = -2
    elif board_temp.turn == 0:
       value = 2
    for element in get_possible_boards ( board_temp ): 
        value_temp = minimax ( element, depth + 1 )       
        if board_temp.turn == 1 and value_temp > value:
               value = value_temp
               the_right_move = element 
        elif board_temp.turn == 0 and value_temp < value:
               value = value_temp
               the_right_move = element 
    if board_temp.turn == 1:
        log.info("max value is {value}".format( value=value ))
    elif board_temp.turn == 0:
        log.info("min value is {value}".format( value=value ))

    if depth == 0:
       return the_right_move
    return value 

def get_possible_boards ( a_board ):
    possible_boards = []
    for cell in get_empty_cells( a_board ):
        if a_board.turn  == 0:
           #updating the newly created board with a mark in one of the empty cells
           new_board = update_board(a_board , cell[0], cell[1])
           new_board.turn = 1 
        elif a_board.turn== 1:
           new_board = update_board(a_board, cell[0], cell[1])
           new_board.turn = 0 
        possible_boards.append(new_board)

    log.info("=========================================")
    for each_board in possible_boards:
        log.info( "possible board: {board}".format(board=each_board.BOARD))
    log.info("=========================================")
    return possible_boards
    
def get_empty_cells ( a_board ):
    empty_cells = []
    for row in range(0, a_board.size): 
        for col  in range(0, a_board.size):
            if  a_board.BOARD[row][col]== ' ':
               empty_cells.append([row, col])
    return empty_cells

def set_players ( selection ):
    if selection == 0:
       first_player = "human"
       second_player = "human"
    elif selection == 1:
       first_player = "human"
       second_player = "computer"
    elif selection == 2:
       first_player = "computer"
       second_player = "computer"
    else:
       print "invalide selection. please enter 0, 1 or 2 to begin" 
    return (first_player, second_player) 

def main():
    print " menu "
    print " enter 0 for human v.s. human"
    print " enter 1 for human v.s. computer"
    print " enter 2 for computer v.s. computer"
    players = set_players (int(raw_input()))
    print players[0]," v.s ",  players[1]
    print " choose size of board. enter 3 or 4 "
    size = int(raw_input())
    board = Board( None, size )
  #  board.player0_moves=[[0,0],[1,1],[1,2]]  #debugging by making fuller boards
  #  board.player1_moves=[[0,2],[0,1],[1,0]]
    while True:
          board.show()
  #        print board.winning_boards
          if board.check_ending == False:
              board = play( board, players[0], players[1])
          elif board.winner == "human":
                 print "human won"
                 break
          elif board.winner == "computer":
                 print "computer won"
                 break
          elif board.draw == True:
                 print "it's a draw! game over"
                 break
    board.show()
     
if __name__ == '__main__':
   main()
   
