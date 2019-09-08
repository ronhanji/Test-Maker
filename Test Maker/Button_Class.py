import pygame
import random

# Function to draw text
def draw_text(surf,pos,text,font,dims=None,font_color=(0,0,0),center=False):
    text_surface = font.render(text, True, font_color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (pos[0]+dims[0]/2,pos[1]+dims[1]/2)
    else:
        text_rect.topleft = pos
    surf.blit(text_surface,text_rect)

# Function to inverse a color
def inverse_color(color):
    return (abs(color[0]-255),abs(color[1]-255),abs(color[2]-255))

class Button():
    def __init__(self, rect, font_name="Arial", fontSize=30, text='', fColor=(150, 150, 150), oColor=(75, 75, 75), visible=True, chng_clr=True, over_color=(75, 75, 75)):
        self.rect = rect
        self.pos = self.rect[:2]
        self.width = self.rect[2]
        self.height = self.rect[3]
        self.text = text
        self.fColor = fColor
        self.oColor = oColor
        self.visible = visible
        self.fontSize = fontSize
        self.font = pygame.font.Font(pygame.font.match_font(font_name), self.fontSize)
        #self.font.set_bold(True)
        self.over_color = over_color
        self.temp=self.fColor
        self.chng_clr = chng_clr
    # a method to draw the button
    def show(self,screen):
        if self.visible:
            pygame.draw.rect(screen,self.fColor,self.rect)
            pygame.draw.rect(screen,self.oColor,self.rect,2)
            self.pos = self.rect[:2]
            self.width = self.rect[2]
            self.height = self.rect[3]
            draw_text(screen,self.pos,self.text,self.font,(self.width,self.height),center=True,font_color=(0,0,0))
    # a method to check if the button is being hovered over
    def isOver(self,mp) -> bool:
        if self.visible:
            if pygame.Rect(self.rect).collidepoint(mp):
                if self.chng_clr:
                    self.fColor = self.over_color
                return True
            else:
                if self.chng_clr:
                    self.fColor = self.temp
        else:
            return False


class TypingBox(Button):
    def __init__(self, rect, font_name="Arial", fontSize=20, initText='', fColor=(150, 150, 150), oColor=(75, 75, 75)
                 , visible=True, chng_clr=True, lineGap=5, autoBoxHeightChng=True, bckspcLim=0):

        super().__init__(rect, font_name, fontSize, initText, fColor, oColor, visible, chng_clr)

        self.words = [x + " " for x in initText.split(" ")]
        self.textHeight = self.font.size("ABCD")[1]
        self.lineGap = lineGap  # extra gap between lines in same box
        self.autoBoxHeightChng = autoBoxHeightChng  # resize height of box based on lines
        self.drawCursor = False  # manually change
        self.bckspcLim = bckspcLim  # amount of characters backspace cannot remove
        if autoBoxHeightChng:
            self.updateBoxHeight(len(self.getLines()))

    def lineTooLong(self, line) -> bool:
        textSize = self.font.size(line)
        return textSize[0] > self.width - self.fontSize//2

    def charInput(self, charVal):
        # backspaces
        if charVal == 8:
            if self.words[-1] == "" and len(self.words) > 1:  # avoid extra backspace
                self.words.pop()
            if len(self.words[0]) > self.bckspcLim:
                self.words[-1] = self.words[-1][:-1]  # remove char from last word in list

        # line breaks
        elif charVal == 13 or charVal == 10:
            if self.words[-1] == "":  # avoid extra backspace
                self.words.pop()
            self.words.append("\n")
            self.words.append("")  # blank string for next word

        # anything else
        else:
            self.words[-1] += chr(charVal)
            if charVal == 32:  # start new word after spacebar
                self.words.append("")

    def getLines(self) -> list:
        lines = list()
        curLine = ""
        for word in self.words:
            if word == "\n":
                lines.append(curLine)
                curLine = ""
            elif self.lineTooLong(curLine + word):
                if curLine != "":  # no spaces == word being typed goes out of bounds
                    lines.append(curLine)
                curLine = word
            else:
                curLine += word
        if not lines or curLine != lines[-1]:  # update currently-being-typed word
            lines.append(curLine)
        return lines

    def updateBoxHeight(self, amountOfLines):
        self.rect[3] = amountOfLines * (self.textHeight + self.lineGap) + self.lineGap


    def iterateCursorBoolean(self) -> bool:
        time = pygame.time.get_ticks()
        return time//500 % 2 == 0

    def show(self,screen, extra=""):
        if self.visible:
            lines = self.getLines()
            if self.autoBoxHeightChng:
                self.updateBoxHeight(len(lines))

            pygame.draw.rect(screen,self.fColor,self.rect)
            pygame.draw.rect(screen,self.oColor,self.rect,2)
            pos = self.rect[:2]
            pos[0] += self.fontSize // 4
            pos[1] += self.lineGap
            if lines and self.drawCursor and self.iterateCursorBoolean():
                lines[-1] += "_"
            else:
                lines[-1] += " "
            lines[-1] += extra
            for line in lines:
                draw_text(screen, pos, line, self.font, (self.width, self.height), center=False,
                          font_color=(0,0,0))
                pos[1] += self.textHeight + self.lineGap
