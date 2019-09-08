import pygame
import random
import Layouts
import QuestionTypes
from Button_Class import Button
from Screen_Class import Screen
from fpdf import FPDF

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
SILVER = (192, 192, 192)


WIDTH = 800
HEIGHT = 600
BGCOLOR = SILVER

# initiate the PDF file
pdf = FPDF()
pdf.add_page()

pdf.set_font("Arial", size=10)
pdf.write(7,"Name:\n")
pdf.write(7,"Date:\n")
pdf.set_font("Arial", size=16)
pdf.cell(200, 10, txt="Test", ln=1, align="C")

pdf.set_font("Courier", size=12)

#initialize pygame as well as the screen and the list of questions
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Maker")
questionLayoutList = list()

scrollBlitPos = [0,-30]


# the Main menu screen
def Main_Menu():
    Main_Menu_options = ['Create Test','Edit Test', 'Exit']
    Main_Menu_buttons = []
    for b in range(len(Main_Menu_options)):
        Main_Menu_buttons.append(Button([WIDTH/2-175/2,b*(50+25)+175,175,50], text=Main_Menu_options[b], fontSize=18))
    menu = Screen((WIDTH,HEIGHT),"Test Maker",25,Main_Menu_buttons,BGCOLOR)
    mp = 0,0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEMOTION:
                mp = pygame.mouse.get_pos()
                for button in menu.buttons:
                    button.isOver(mp)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in menu.buttons:
                    ## CHangE OPTIONS
                    if button.isOver(mp):
                        return button.text
        menu.draw(screen)
        pygame.display.flip()

# The options screen
def Options_Menu(saveIndex = -1):
    options = ["Multiple Choice","Fill in The Blanks","Ordering","True and False",
    "Standard","Connecting"]
    option_buttons = []
    option_buttons.append(Button((0,HEIGHT-50,175,50),text="Back"))
    for b in range(len(options)):
        option_buttons.append(Button([WIDTH/2-175/2,b*(50+25)+100,175,50], text=options[b], fontSize=18))
    options = Screen((WIDTH,HEIGHT),"Options",25,option_buttons,BGCOLOR)
    mp = 0,0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            if event.type == pygame.MOUSEMOTION:
                mp = pygame.mouse.get_pos()
                for button in options.buttons:
                    button.isOver(mp)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in options.buttons:
                    if button.isOver(mp):
                        response= button.text
                        if response == "Multiple Choice":
                            qstn = QuestionTypes.MC("", ["", ""])
                            layout = Layouts.MultipleChoiceLayout(qstn, defaultRect.copy())
                        elif response == "Fill in The Blanks":
                            qstn = QuestionTypes.FITB("")
                            layout = Layouts.FITBQuestionLayout(qstn, defaultRect.copy())
                        elif response == "Ordering":
                            qstn = QuestionTypes.Ordering("", ["", ""])
                            layout = Layouts.OrderingLayout(qstn, defaultRect.copy())
                        elif response == "True and False":
                            qstn = QuestionTypes.True_False("")
                            layout = Layouts.TrueFalseLayout(qstn, defaultRect.copy())
                        elif response == "Standard":
                            qstn = QuestionTypes.Normal("")
                            layout = Layouts.NormalQuestionLayout(qstn, defaultRect.copy())
                        elif response == "Connecting":
                            qstn = QuestionTypes.Connecting("", ["", ""], ["", ""])
                            layout = Layouts.ConnectingQuestionLayout(qstn, defaultRect.copy())
                        elif response == "Back":
                            return "Menu"
                        response = Question_Editor(layout,saveIndex)
                        return response

        options.draw(screen)
        pygame.display.flip()

def Question_Editor(questionLayout, saveIndex=-1):
    global questionData, questionLayoutList

    if saveIndex == -1:
        saveIndex = len(questionLayoutList)
    questionLayout.save()
    back = Button((0,HEIGHT-50,175,50),text="Back")
    save = Button((175,HEIGHT-50,175,50),text="Save")
    reset = Button((350,HEIGHT-50,175,50),text="Reset")

    selBox = None
    pygame.key.set_repeat(500, 25)
    mp = 0,0
    saved = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEMOTION:
                mp = pygame.mouse.get_pos()
                questionLayout.isOver(mp)
                back.isOver(mp)
                save.isOver(mp)
                reset.isOver(mp)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if selBox is not None:
                    selBox.drawCursor = False
                selBox = questionLayout.isOver(mp)
                if selBox is not None:
                    selBox.drawCursor = True

                questionLayout.checkButtonClick(mp)

                if back.isOver(mp):
                    return "Create Test"
                elif save.isOver(mp):
                    if questionLayout.save():
                        questionLayoutList.insert(saveIndex,questionLayout)
                        return "Create Test"
                    else:
                        pass
                    #saved = True
                elif reset.isOver(mp):
                    questionLayout.reset()

            if event.type == pygame.KEYDOWN:
                if selBox is not None:
                    char = event.unicode
                    if char:  # keys like shift return None
                        selBox.charInput(ord(char))

        screen.fill(BGCOLOR)
        back.show(screen)
        save.show(screen)
        reset.show(screen)
        questionLayout.show(screen)
        pygame.display.flip()

def orderLayouts(rectList):
    currentY = 150
    for rect in rectList:
        rect[1] = currentY
        currentY += rect[3]


def All_Questions_Screen():
    global WIDTH, questionLayoutList, screen, scrollBlitPos

    if not questionLayoutList: # should probably do something more here, right now it just refuses
        return "Menu"

    rectList = [layout.rect for layout in questionLayoutList]
    orderLayouts(rectList)
    scrollSurfaceHeight = rectList[-1][1] + rectList[-1][3] + 30
    scrollSurface = pygame.Surface((WIDTH, scrollSurfaceHeight))


    buttons = list()
    buttonHeight = 25
    buttonWidth = 75
    buttonTexts = ["Back", "Up", "Down"]
    for rect in rectList:
        currentY = rect[1] - buttonHeight
        currentX = 0
        for text in buttonTexts:
            buttons.append(Button([currentX,currentY,buttonWidth,buttonHeight],text=text, fontSize=20))
            currentX += buttonWidth
        currentX = rect[2] - 150
        buttons.append((Button([currentX,currentY-25,100,50],text="Add Question",fontSize=15)))
        buttons.append((Button([currentX + 100, currentY-25, 100, 50], text="Edit Question", fontSize=15)))
    if rectList:
        currentY = rectList[-1][1] + rectList[-1][3]
        buttons.append((Button([currentX, currentY - 25, 100, 50], text="Add Question", fontSize=15)))
    mp = [0, 0]
    while True:
        screen.fill(BGCOLOR)
        scrollSurface.fill(BGCOLOR)
        for layout in questionLayoutList:
            layout.show(scrollSurface)
        for b in buttons:
            b.show(scrollSurface)
        screen.blit(scrollSurface, scrollBlitPos)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Exit"
            if event.type == pygame.MOUSEMOTION:
                mp = list(pygame.mouse.get_pos())
                mp[1] -= scrollBlitPos[1]
                for b in buttons:
                    b.isOver(mp)
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button == 5:  # scroll down
                    if scrollBlitPos[1] >= 15 or scrollBlitPos[1] >= HEIGHT - scrollSurfaceHeight:
                        scrollBlitPos[1] -= 15
                        print(event.button, scrollBlitPos)
                elif event.button == 4:  # scroll up
                    if scrollBlitPos[1] <= -45:
                        scrollBlitPos[1] += 15
                        print(event.button, scrollBlitPos)
                else:  # left click
                    for num, b in enumerate(buttons):
                        num = num//5
                        if b.isOver(mp):
                            if b.text == "Back":
                                return "Menu"
                            elif b.text == "Up":
                                if num > 0:
                                    temp = questionLayoutList[num-1]
                                    questionLayoutList[num-1] = questionLayoutList[num]
                                    questionLayoutList[num] = temp
                                    return "Edit Test"
                            elif b.text == "Down":
                                if num < len(questionLayoutList)-1:
                                    temp = questionLayoutList[num+1]
                                    questionLayoutList[num+1] = questionLayoutList[num]
                                    questionLayoutList[num] = temp
                                    return "Edit Test"
                            elif b.text == "Add Question":
                                Options_Menu(saveIndex=num)
                                return "Edit Test"
                            elif b.text == "Edit Question":
                                oldLen = len(questionLayoutList)
                                curentlyInEditing = questionLayoutList[num]
                                curentlyInEditing.rect[1] = defaultRect[1]
                                Question_Editor(curentlyInEditing, saveIndex=num)
                                if oldLen != len(questionLayoutList):
                                    questionLayoutList.pop(num+1)
                                return "Edit Test"


left = WIDTH // 2 - 250
top = HEIGHT // 2 - 100
defaultRect = [left, top, 500, 200]

response="Menu"
while True:
    if response == "Menu":
        response = Main_Menu()
    elif response =="Create Test":
        response = Options_Menu()
    elif response == "Edit Test":
        response = All_Questions_Screen()

    else:
        # Once you exit the program, save the question unto a pdf file
        for num, question in enumerate(questionLayoutList):
            question.question.writeToFile(pdf,num+1,9,7)
            pdf.write(9, "\n")
        break
# save the pdf file created
pdf.output("test.pdf")
pygame.quit()
