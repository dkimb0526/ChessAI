#!/usr/bin/env python
# coding: utf-8

# In[1]:


import Chess_pieces
import pygame
import chess
import math


# In[2]:


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


# In[3]:


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


# In[ ]:


def update(scrn, board):
    '''
    Updates the screen based on the board class
    '''

    for i in range(64):
        piece = board.piece_at(i)
        if piece is None:
            continue
        else:
            piece_image = pieces[str(piece)]
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


# In[4]:


def main(BOARD):

    '''
    for human vs human game
    '''
    #make background black
    scrn.fill(BLACK)
    #name window
    pygame.display.set_caption('Chess')
    
    #variable to be used later
    index_moves = []

    status = True
    while (status):
        #update screen
        update(scrn,BOARD)

        for event in pygame.event.get():
     
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                status = False

            # if mouse clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                #remove previous highlights
                scrn.fill(BLACK)
                #get position of mouse
                pos = pygame.mouse.get_pos()

                #find which square was clicked and index of it
                square = (math.floor(pos[0]/100),math.floor(pos[1]/100))
                index = (7-square[1])*8+(square[0])
                
                # if we are moving a piece
                if index in index_moves: 
                    
                    move = moves[index_moves.index(index)]
                    
                    BOARD.push(move)

                    #reset index and moves
                    index=None
                    index_moves = []
                    
                    
                # show possible moves
                else:
                    #check the square that is clicked
                    piece = BOARD.piece_at(index)
                    #if empty pass
                    if piece == None:
                        
                        pass
                    else:
                        
                        #figure out what moves this piece can make
                        all_moves = list(BOARD.legal_moves)
                        moves = []
                        for m in all_moves:
                            if m.from_square == index:
                                
                                moves.append(m)

                                t = m.to_square

                                TX1 = 100*(t%8)
                                TY1 = 100*(7-t//8)

                                
                                #highlight squares it can move to
                                pygame.draw.rect(scrn,BLUE,pygame.Rect(TX1,TY1,100,100),5)
                        
                        index_moves = [a.to_square for a in moves]
     
    # deactivates the pygame library
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    pygame.quit()


# In[5]:



pygame.init()
b = chess.Board()
main(b)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[9]:




def main_one_agent(BOARD,agent,agent_color):
    
    '''
    for agent vs human game
    color is True = White agent
    color is False = Black agent
    '''
    
    #make background black
    scrn.fill(BLACK)
    #name window
    pygame.display.set_caption('Chess')
    
    #variable to be used later
    index_moves = []

    status = True
    while (status):
        #update screen
        update(scrn,BOARD)
        
     
        if BOARD.turn==agent_color:
            BOARD.push(agent(BOARD))
            scrn.fill(BLACK)

        else:

            for event in pygame.event.get():
         
                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.QUIT:
                    status = False

                # if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #reset previous screen from clicks
                    scrn.fill(BLACK)
                    #get position of mouse
                    pos = pygame.mouse.get_pos()

                    #find which square was clicked and index of it
                    square = (math.floor(pos[0]/100),math.floor(pos[1]/100))
                    index = (7-square[1])*8+(square[0])
                    
                    # if we have already highlighted moves and are making a move
                    if index in index_moves: 
                        
                        move = moves[index_moves.index(index)]
                        #print(BOARD)
                        #print(move)
                        BOARD.push(move)
                        index=None
                        index_moves = []
                        
                    # show possible moves
                    else:
                        
                        piece = BOARD.piece_at(index)
                        
                        if piece == None:
                            
                            pass
                        else:

                            all_moves = list(BOARD.legal_moves)
                            moves = []
                            for m in all_moves:
                                if m.from_square == index:
                                    
                                    moves.append(m)

                                    t = m.to_square

                                    TX1 = 100*(t%8)
                                    TY1 = 100*(7-t//8)

                                    
                                    pygame.draw.rect(scrn,BLUE,pygame.Rect(TX1,TY1,100,100),5)
                            #print(moves)
                            index_moves = [a.to_square for a in moves]
     
    # deactivates the pygame library
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    pygame.quit()


# In[10]:




def main_two_agent(BOARD,agent1,agent_color1,agent2):
    '''
    for agent vs agent game
    
    '''
  
    #make background black
    scrn.fill(BLACK)
    #name window
    pygame.display.set_caption('Chess')
    
    #variable to be used later

    status = True
    while (status):
        #update screen
        update(scrn,BOARD)
        
        if BOARD.turn==agent_color1:
            BOARD.push(agent1(BOARD))

        else:
            BOARD.push(agent2(BOARD))

        scrn.fill(BLACK)
            
        for event in pygame.event.get():
     
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                status = False
     
    # deactivates the pygame library
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    pygame.quit()


# In[11]:





# In[ ]:





# In[ ]:




