from Button_Class import *
import pygame

# a method to create a screen
class Screen():
    def __init__(self, dimensions, titleText,topYPos,buttons,BGCOLOR, fontType = "arial", titleSize= 20):
        
        self.menuTitleSize = titleSize
        self.mainTitleFont = pygame.font.Font(pygame.font.match_font(fontType), self.menuTitleSize)
        self.menuTitle = titleText
        self.BGCOLOR = BGCOLOR
        yposMenu = topYPos
        mainTitleSize =  self.mainTitleFont.size(self.menuTitle)
        self.mainTitlePos = (dimensions[0]//2 - mainTitleSize[0]//2, yposMenu)
        self.buttons = buttons

    def draw(self, win):
        win.fill(self.BGCOLOR)
        draw_text(win, self.mainTitlePos, self.menuTitle, self.mainTitleFont)
        for button in self.buttons:
            button.show(win)
