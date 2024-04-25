from pyparsing import White
from Arena import Arena 
from Agent import HumanReversiPlayer, MonteCarloTreeSearch, Agent
from HeuristicMonteCarloTreeSearch import HeuristicMonteCarloTreeSearch
from EnvState import Reversi 

import pygame
from GameGraphics import *

class Play:
    BOARD_SIZE = 8
    
    def __init__(self) -> None:
        self.playas = 0

        self.game = Reversi()
        
        self.computer = MonteCarloTreeSearch(self.game, "AI")
        self.human = HumanReversiPlayer(self.game, "PLAYER")
    
        self.competitors : list[Agent] = [self.computer, self.computer] 
        
        self.move = True
        self.decision_given = False
        
        self.delay = False
        self.turn_time = 0
        
        self.turn = 0
        self.valid = True
        self.invalid_time = 0
        
        
        ## Graphic ##
        self.initGraphic()
        
    def init(self):
        if self.mode == self.ModeOptions['pvp']:
            self.competitors[self.playas] = self.human
            self.competitors[self.playas + 1] = self.human
        
        if self.mode == self.ModeOptions['pva']:
            self.competitors[self.playas] = self.human
        
        if self.mode == self.ModeOptions['ava']:
            self.delay = True
            self.turn_time = 5
            self.move = False
        
        self.competitors[0].setName(self.black_name[self.mode])
        self.competitors[1].setName(self.white_name[self.mode])
        
        self.playground = Arena(self.game, self.competitors) 
        
        self.board = self.playground._Arena__cannonical_state.board2D
        self.replay = False
    
    def initGraphic(self):
        self.mode = 1
        self.ModeOptions = { 'pvp' : 0 , 'pva' : 1, 'ava' : 2}
        self.black_name = ["Smart Guy" , "Human", "Doraemon"]
        self.white_name = ["Cute Girl" , "Doraemon", "Tama"]
        
        self.board = [[1 for j in range(self.BOARD_SIZE)] for i in range(self.BOARD_SIZE) ]
        self.valid_move = [[False for j in range(self.BOARD_SIZE)] for i in range(self.BOARD_SIZE) ]
        self.valid_move_count = 0
        
        self.text = Text()
        
        self.ai_img = [
                        Image("data/img/dark_doraemon.png"),
                        Image("data/img/tama.png")
                    ]
        self.player_img = [
                            Image("data/img/player.png"),
                            Image("data/img/player2.png")
                        ]
        
        self.white = Image("data/img/white.png")
        self.black = Image("data/img/black.png")
        
        self.select = [
                        Image("data/img/bla_slt_sqr.png"),
                        Image("data/img/whi_slt_sqr.png")
                     ]
        self.valid_square = [
                        Image("data/img/bla_valid_sqr.png"),
                        Image("data/img/whi_valid_sqr.png")
                     ]
        
        self.current_x = 4
        self.current_y = 4
        
        self.white_score = 2
        self.black_score = 2
        
        self.count_time = -1
        self.frame_time = 5
        
        self.result_img = Image("data/img/result.png")
        self.battle_ending = False
        self.winner = "noone"
      
    def show(self, surface):
        self.showTheme(surface)
        self.showPlayer(surface)
        self.showScore(surface)
        
        self.handleAction(surface)
        self.showInvalid(surface)
        self.showResult(surface)
    
    def handleAction(self, surface):
        if self.battle_ending == True:
            return   
        
        if len(self.playground._Arena__cannonical_state.legal) > 0:
            
            if self.delay:
                self.turn_time -= 1
                if self.turn_time == 0:
                    self.decision_given = True
            
            if self.decision_given == True:
                edge = ()
                a = self.playground._Arena__agents_list[self.playground._Arena__cannonical_state.player] 
                if a.get_agent_type() == "HUMAN":
                    choice = self.getChoice(self.current_x, self.current_y)
                    self.valid = a.deliberate(choice)
                    
                    self.decision_given = False
                    
                    if self.valid == False:
                        self.invalid_time = 10
                        return
                    
                    if self.mode == self.ModeOptions['pva']:
                        self.move = False
                        self.delay = True
                        self.turn_time = 5
                    
                
                if a.get_agent_type() == "AI":
                    a.deliberate()
                    
                    
                    self.decision_given = False

                    if self.mode == self.ModeOptions['pva']:
                        self.move = True
                    
                    if self.mode == self.ModeOptions['ava']:
                        self.delay = True
                        self.turn_time = 5
                     
                edge = a.act()

                for oa in self.playground._Arena__agents_list: 
                    if oa is not a: 
                        oa.notify()
                        
                
                self.turn += 1
                self.turn %= 2
                print(self.playground._Arena__cannonical_state)
                print("{} played : {}".format(a.name, edge))
            
            else:
                a = self.playground._Arena__agents_list[self.playground._Arena__cannonical_state.player] 
                if a.get_agent_type() == "HUMAN":
                    for i in range(self.BOARD_SIZE):
                        for j in range(self.BOARD_SIZE):
                            choice = self.getChoice(i , j)
                            
                            self.valid_move[i][j] = a.deliberate(choice)
                            
                if a.get_agent_type() == 'AI':
                    for i in range(self.BOARD_SIZE):
                        for j in range(self.BOARD_SIZE):
                            choice = self.getChoice(i , j)
                            
                            self.valid_move[i][j] = a.checkLegal(choice)
                            
                self.valid_move_count = 0
                for i in range(self.BOARD_SIZE):
                    for j in range(self.BOARD_SIZE):
                        if self.valid_move[i][j]:
                            self.valid_move_count += 1
                            
                if self.valid_move_count == 0:
                    self.battle_ending = True
                    self.winner = self.playground.getWinner()      
                    if self.winner == 'None':
                        self.winner = 'Draw'  
                    else: 
                        self.winner += " win"
            
            
    
    def showResult(self, surface):
        if self.battle_ending:
            self.result_img.show(surface)
            
            self.text.setColor((0 , 255, 0))
            self.text.setText(self.winner)
            self.text.setSize(60)
            self.text.setRect(pygame.Rect(0 , 200 , 1280 , 200))
            self.text.show(surface)
            
    def getChoice(self, x , y):
        return chr(ord('A') + x) + str(y + 1)
    def calculateScore(self):
        self.white_score = 0
        self.black_score = 0
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == 2:
                    self.white_score += 1
                if self.board[i][j] == 1:
                    self.black_score += 1  
    def showTheme(self, surface):   
        drawRect(surface, (235, 138, 95), pygame.Rect(0 , 0 , 1280 , 720))
        
            
        drawRect(surface, (73, 146, 123), pygame.Rect(30 , 440 , 240 , 200))
        drawRect(surface, (73, 146, 123), pygame.Rect(1250 - 240 , 440 , 240 , 200))
        
        drawImage(surface, self.black.image, 30 + 83, 460)
        drawImage(surface, self.white.image, 1250 - 240 + 83, 460)
        
        board_x = 340
        board_y = 60
        tile_size = 75
        border_size = 45
        
        drawRect(surface , (129, 104, 94), (board_x - border_size, board_y - border_size, tile_size * 8 + border_size * 2, tile_size * 8 + border_size * 2))
        drawRect(surface , (0 , 0 , 0), (board_x - 2, board_y - 2 , tile_size * 8 + 4 , tile_size * 8 + 4))
        self.text.setSize(30)
        
        self.text.setColor(pygame.Color(255 , 255 , 255))
        for i in range(self.BOARD_SIZE):
            cha = chr(ord('A') + i)
            self.text.setText(cha)
            self.text.setRect(pygame.Rect(board_x + i * tile_size, 25, tile_size, 25))
            self.text.show(surface)
            
        for i in range(self.BOARD_SIZE):
            cha = str(i + 1)
            self.text.setText(cha)
            self.text.setRect(pygame.Rect(board_x - border_size, board_y + i * tile_size , border_size, tile_size))
            self.text.show(surface)
        
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                rect = pygame.Rect(board_x + i * tile_size, board_y + j * tile_size , tile_size - 1, tile_size - 1)
                drawRect(surface, (73, 146, 123), rect)
                
                if self.board[j][i] == 1:
                    self.black.setPos(board_x + i * tile_size, board_y + j * tile_size)
                    self.black.show(surface)
                    
                if self.board[j][i] == 2:
                    self.white.setPos(board_x + i * tile_size, board_y + j * tile_size)
                    self.white.show(surface)
                    
                if self.move == True and i == self.current_x and j == self.current_y:
                    self.select[self.turn].setPos(board_x + i * tile_size, board_y + j * tile_size)
                    self.select[self.turn].show(surface)     
                    
                if self.valid_move[i][j] == True:
                    self.valid_square[self.turn].setPos(board_x + i * tile_size, board_y + j * tile_size)
                    self.valid_square[self.turn].show(surface) 
    def showPlayer(self, surface):
        self.text.setColor(pygame.Color(0 , 0 , 0))
        self.text.setSize(30)
        
        if self.mode == self.ModeOptions['pvp']:
            self.player_img[0].setPos(30, 300 - self.player_img[1].image.get_height())
            self.player_img[0].show(surface)
            
            self.player_img[1].setPos(1250 - self.player_img[1].image.get_width() , 300 - self.player_img[1].image.get_height())
            self.player_img[1].show(surface)
            
            
        if self.mode == self.ModeOptions['pva']:
            self.player_img[0].setPos(30, 300 - self.player_img[1].image.get_height())
            self.player_img[0].show(surface)
            
            self.ai_img[0].setPos(1250 - self.player_img[1].image.get_width() , 300 - self.ai_img[0].image.get_height())
            self.ai_img[0].show(surface)
            
            
        if self.mode == self.ModeOptions['ava']:
            self.ai_img[0].setPos(30, 300 - self.ai_img[0].image.get_height())
            self.ai_img[0].show(surface)
            
            self.ai_img[1].setPos(1250 - self.ai_img[1].image.get_width() , 300 - self.ai_img[1].image.get_height())
            self.ai_img[1].show(surface)
        
        
        self.text.setText(self.black_name[self.mode])
        self.text.setRect(pygame.Rect(30 , 220, 240 , 220))
        self.text.show(surface)
        
        self.text.setColor(pygame.Color(255 , 255 , 255))        
        self.text.setText(self.white_name[self.mode])
        self.text.setRect(pygame.Rect(1250 - 240 , 220, 240 , 220))
        self.text.show(surface)
            
        
        if self.turn == 0:
            self.text.setColor(pygame.Color(0 , 0 , 0))
            self.text.setText("[ Black is thinking...! ]")
            self.text.setRect(pygame.Rect(30 , 260, 240 , 260))
        else:
            self.text.setColor(pygame.Color(255 , 255 , 255))
            self.text.setText("[ White is thinking...! ]") 
            self.text.setRect(pygame.Rect(1250 - 240 , 260, 240 , 260))
            
        self.text.setSize(20)
        self.text.show(surface) 
        self.text.setSize(35)
    def showInvalid(self, surface):
        if self.valid == False:
            
            self.text.setColor(pygame.Color(255 , 0 , 0))
            self.text.setSize(35)
            self.text.setText("A fucking invalid move!")
            self.text.setRect(pygame.Rect(0 , 0, 1280 , 720))
            self.text.show(surface)   
            
            self.invalid_time -= 1
            if self.invalid_time == 0:
                self.valid = True
                                                     
    def showScore(self, surface):
        self.calculateScore()
        
        self.text.setColor(pygame.Color(0 , 0 , 0))
        self.text.setText(str(self.black_score))
        self.text.setRect(pygame.Rect(30 , 580, 240 , 0))
        self.text.show(surface)
        
        self.text.setColor(pygame.Color(255 , 255 , 255))
        self.text.setText(str(self.white_score))
        self.text.setRect(pygame.Rect(1250 - 240 , 580, 240 , 0))
        self.text.show(surface)   
        
    def keyUp(self, e):
        if e == pygame.K_DOWN or e == pygame.K_UP or e == pygame.K_LEFT or e == pygame.K_RIGHT:
            self.count_time = -1    
        
        if e == pygame.K_RETURN:
            self.decision_given = True
            
        if self.battle_ending:
            self.replay = True
    def keyPressed(self, e):
        if e == pygame.K_DOWN or e == pygame.K_UP or e == pygame.K_LEFT or e == pygame.K_RIGHT:
            self.count_time += 1
            self.count_time %= self.frame_time
            
        if self.count_time == 0:
            if e == pygame.K_DOWN:
                self.current_y += 1
            
            if e == pygame.K_UP:
                self.current_y += self.BOARD_SIZE - 1
            
            if e == pygame.K_LEFT:
                self.current_x += self.BOARD_SIZE - 1
            
            if e == pygame.K_RIGHT:
                self.current_x += 1   
                
            self.current_x %= self.BOARD_SIZE
            self.current_y %= self.BOARD_SIZE 