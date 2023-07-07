#!/usr/bin/env python
# coding: utf-8

# In[1]:


import Chess_pieces
import pygame
import chess
import math
import random
from copy import deepcopy
import chess.polyglot
#from AI import random_agent


# In[2]:


reader = chess.polyglot.open_reader('baron30.bin')


# In[3]:


# Resize the image to a specific size
new_size = (90, 90)  # Set the desired size
#names
b_pawn = pygame.transform.scale(pygame.image.load('Chess_pieces//b_pawn.png'), new_size)
b_knight = pygame.transform.scale(pygame.image.load('Chess_pieces//b_knight.png'), new_size)
b_bishop = pygame.transform.scale(pygame.image.load('Chess_pieces//b_bishop.png'), new_size)
b_rook = pygame.transform.scale(pygame.image.load('Chess_pieces//b_rook.png'), new_size)
b_queen = pygame.transform.scale(pygame.image.load('Chess_pieces//b_queen.png'), new_size)
b_king = pygame.transform.scale(pygame.image.load('Chess_pieces//b_king.png'), new_size)
w_pawn = pygame.transform.scale(pygame.image.load('Chess_pieces//w_pawn.png'), new_size)
w_knight = pygame.transform.scale(pygame.image.load('Chess_pieces//w_knight.png'), new_size)
w_bishop = pygame.transform.scale(pygame.image.load('Chess_pieces//w_bishop.png'), new_size)
w_rook = pygame.transform.scale(pygame.image.load('Chess_pieces//w_rook.png'), new_size)
w_queen = pygame.transform.scale(pygame.image.load('Chess_pieces//w_queen.png'), new_size)
w_king = pygame.transform.scale(pygame.image.load('Chess_pieces/w_king.png'), new_size)


# In[4]:


#initialise display
X = 800
Y = 800
scrn = pygame.display.set_mode((X, Y))

#basic colours
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

#initialise chess board
pygame.init()
b = chess.Board()

#load piece images
pieces = {'p': b_pawn.convert(),
          'n': b_knight.convert(),
          'b': b_bishop.convert(),
          'r': b_rook.convert(),
          'q': b_queen.convert(),
          'k': b_king.convert(),
          'P': w_pawn.convert(),
          'N': w_knight.convert(),
          'B': w_bishop.convert(),
          'R': w_rook.convert(),
          'Q': w_queen.convert(),
          #'K': pygame.image.load('Chess_pieces//w_king.png').convert(),
          'K': w_king.convert()
          
          }


# In[5]:


def update(scrn, board):
    scrn.fill(BLACK)

    for i in range(64):
        piece = board.piece_at(i)
        if piece is None:
            continue
        else:
            piece_image = pieces[piece.symbol()]
            piece_rect = piece_image.get_rect()

            # Calculate the position to center the piece
            x = (i % 8) * 100 + (100 - piece_rect.width) // 2
            y = 700 - (i // 8) * 100 + (100 - piece_rect.height) // 2

            scrn.blit(piece_image, (x, y))

    for i in range(7):
        i = i + 1
        pygame.draw.line(scrn, WHITE, (0, i * 100), (800, i * 100))
        pygame.draw.line(scrn, WHITE, (i * 100, 0), (i * 100, 800))

    pygame.display.flip()


# In[6]:


scoring = {'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0,
           'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}

def eval_board(board):
    score = 0
    pieces = board.piece_map()
    for key in pieces:
        score += scoring[str(pieces[key])]

    return score

def eval_space(board):
    no_moves = len(list(board.legal_moves))
    value = (no_moves / (20 + no_moves))

    if board.turn:
        return value
    else:
        return -value

def min_maxN(board, N, reader):
    #print("min_maxN called with N =", N)  # Debug message

    opening_move = reader.get(board)
    if opening_move is not None:
        #print("Found opening move:", opening_move.move)  # Debug message
        return opening_move.move

    moves = list(board.legal_moves)
    scores = []

    for move in moves:
        temp = board.copy()
        temp.push(move)
        outcome = temp.outcome()

        if outcome is None:
            if N > 1:
                #print("Recursing with N =", N-1)  # Debug message
                temp_best_move = min_maxN(temp, N-1, reader)
                temp.push(temp_best_move)

            scores.append(eval_board(temp))

        elif temp.is_checkmate():
            #print("Checkmate found:", move)  # Debug message
            return move

        else:
            val = 1000
            if board.turn:
                scores.append(-val)
            else:
                scores.append(val)

        scores[-1] = scores[-1] + eval_space(temp)

    if board.turn:
        best_move = moves[scores.index(max(scores))]
    else:
        best_move = moves[scores.index(min(scores))]

    #print("Returning best move:", best_move)  # Debug message
    return best_move


# In[7]:


def play_game(board, agent, agent_color, reader):
    index_moves = []
    highlighted_squares = []

    # Main game loop
    while True:
        # Update the screen
        if not highlighted_squares:
            update(scrn, board)

        # Check for game over conditions
        if board.is_game_over():
            print("Game Over")
            print("Result: " + board.result())
            #pygame.quit()
            break

        # Agent's turn
        if board.turn == agent_color:
            move = agent(board, reader)  # Pass 'reader' to the agent function
            board.push(move)

        # Human player's turn
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    update(scrn, board)
                    pos = pygame.mouse.get_pos()
                    square = (math.floor(pos[0] / 100), math.floor(pos[1] / 100))
                    index = (7 - square[1]) * 8 + square[0]
                    highlighted_squares = []

                    if index in index_moves:
                        move = moves[index_moves.index(index)]
                        board.push(move)
                        index_moves = []
                        highlighted_squares = []
                    else:
                        piece = board.piece_at(index)
                        if piece is not None:
                            all_moves = list(board.legal_moves)
                            moves = []
                            for m in all_moves:
                                if m.from_square == index:
                                    moves.append(m)
                                    t = m.to_square
                                    highlighted_squares.append((t % 8, 7 - t // 8))
                            index_moves = [m.to_square for m in moves]

        # Draw highlighted squares
        for square in highlighted_squares:
            TX1 = 100 * square[0]
            TY1 = 100 * square[1]
            pygame.draw.rect(scrn, BLUE, pygame.Rect(TX1, TY1, 100, 100), 5)

        pygame.display.flip()


# In[8]:


def min_max1(BOARD, reader):
    return min_maxN(BOARD, 1, reader)
def min_max2(BOARD, reader):
    return min_maxN(BOARD, 2, reader)
def min_max3(BOARD, reader):#takes too long to make calculations
    return min_maxN(BOARD, 3, reader)


# In[9]:


play_game(b, min_max3, chess.BLACK, reader)


# In[10]:


pygame.quit()


# In[ ]:




