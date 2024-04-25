import pygame
import enum

from GameMenu import *
from GamePlay import *

class Scene(enum.Enum):
    menu = 1
    play = 2
    

class Display:
    
    def __init__(self) -> None:
        self.scene = Scene.menu
        
        self.menu = Menu()
        self.play = Play()
        
    
    def show(self, surface):
        
        if self.scene == Scene.menu:
            self.menu.show(surface)
            
        if self.scene == Scene.play:
            self.play.show(surface)
    
    def keyUp(self, e):
        if self.scene == Scene.menu:
            self.menu.keyUp(e) 
            
            if self.menu.mode != -1:
                self.scene = Scene.play
                self.play.mode = self.menu.mode
                self.play.init()
                return
                
        
        if self.scene == Scene.play:
            self.play.keyUp(e)
            if self.play.replay == True:
                self.scene = Scene.menu
                self.menu = Menu()
                self.play = Play()
               
    
    def keyPressed(self, e):
        if self.scene == Scene.menu:
            self.menu.keyPressed(e)
            
        if self.scene == Scene.play:
            self.play.keyPressed(e)
            