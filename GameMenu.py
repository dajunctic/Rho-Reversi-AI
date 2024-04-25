import enum
from turtle import home
from GameGraphics import *

class MenuPages(enum.Enum):
    home = 1
    rule = 2
    mode = 3

class Menu:
    def __init__(self) -> None:
        
        self.page = MenuPages.home
        
        ######################################################
        #######################  HOME ########################
        self.home_img = Image("data/img/home.png")
        self.select_img = Image("data/img/select.png")
        self.select2_img = Image("data/img/select2.png")
        self.menu_img = Image("data/img/menu.png")
        
        self.current_choice = 0
        self.total_choice = 3
        
        self.count_time = -1
        self.frame_time = 10
        
        self.quit = False
        
        self.MenuOptions = { 'play' : 0, 'rule': 1,  'quit' : 2}
        
        
        ######################################################
        ######################## MODE ########################
        self.mode_img = Image("data/img/mode.png")
        
        self.current_mode = 0
        self.total_mode = 3
        
        self.mode = -1
        
        ######################################################
        ######################## RULE ########################
        self.rule_img = [
                        Image("data/img/rule1.png"),
                        Image("data/img/rule2.png"),
                        Image("data/img/rule3.png"),
                        Image("data/img/rule4.png")
                    ]
        self.current_rule = 0
        
    
    def show(self, surface):
        self.home_img.show(surface)
        
        if self.page == MenuPages.home:
            x = 640
            y = self.current_choice * 75 + 277
            self.select2_img.setPos(x, y)
            self.select2_img.show(surface)
            
            self.menu_img.show(surface)
            
        if self.page == MenuPages.rule:
            self.rule_img[self.current_rule].show(surface)
            
        if self.page == MenuPages.mode:
            x = 655
            y = self.current_mode * 100 + 259
            self.select2_img.setPos(x, y)
            self.select2_img.show(surface)
            
            self.mode_img.show(surface)
            
    
    def keyUp(self, e):
        if e == pygame.K_DOWN or e == pygame.K_UP:
            self.count_time = -1 
            
        if e == pygame.K_RETURN:
            if self.page == MenuPages.home:
                if self.current_choice == self.MenuOptions['quit']:
                    self.quit = True
                if self.current_choice == self.MenuOptions['play']:
                    self.page = MenuPages.mode
                    
                if self.current_choice == self.MenuOptions['rule']:
                    self.page = MenuPages.rule
                return
                    
            if self.page == MenuPages.mode:
                self.mode = self.current_mode
            
            if self.page == MenuPages.rule:
                self.current_rule += 1
                if self.current_rule == len(self.rule_img):
                    self.page = MenuPages.home
                    self.current_rule = 0
    
    def keyPressed(self, e):
        if e == pygame.K_DOWN:
            
            self.count_time += 1
            self.count_time %= self.frame_time
            
            if self.page == MenuPages.home:    
                if self.count_time == 0:
                    self.current_choice += 1
                    self.current_choice %= self.total_choice
            if self.page == MenuPages.mode:
                if self.count_time == 0:
                    self.current_mode += 1
                    self.current_mode %= self.total_mode
                    
        if e == pygame.K_UP:
            
            self.count_time += 1
            self.count_time %= self.frame_time
            
            if self.page == MenuPages.home:    
                if self.count_time == 0:
                    self.current_choice += self.total_choice - 1
                    self.current_choice %= self.total_choice
            if self.page == MenuPages.mode:
                if self.count_time == 0:
                    self.current_mode += self.total_mode - 1
                    self.current_mode %= self.total_mode