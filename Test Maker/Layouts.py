from typing import List, Dict, Callable

import pygame
import QuestionTypes
import Button_Class
from Button_Class import TypingBox
import random

class Layout:

    def __init__(self, question, rect, editing=False):
        self.question = question
        self.rect = rect
        self.questionTypingBox = None # init in self.genBoxes()
        self.typingBoxes = list()     # init in self.genBoxes()
        self.buttons = dict()  # dict[Button : Callable], Callable being functions in this class
        self.genBoxes(not editing)
        self.genButtons()

    def genBoxes(self, new=False):
        self.typingBoxes = list() # reset list
        rect = self.rect[:3] + [10] #10 can be any number, it changes based on font automatically (height)
        questionBox = Button_Class.TypingBox(rect=rect, initText=self.question.questionText)
        self.questionTypingBox = questionBox
        self.typingBoxes.append(questionBox)

    def genButtons(self):
        self.buttons = dict()  # reset list

    def orderBoxes(self, list, startRect, addInitWidth=True):
        if len(list) < 1:
            return
        currentY = startRect[1]
        if addInitWidth:
            currentY+= startRect[3]
        for box in list:
            box.rect[1] = currentY
            currentY += box.rect[3]

    def updateHeight(self):
        self.rect[3] = self.questionTypingBox.rect[1] + self.questionTypingBox.rect[3] - self.rect[1] + 100

    def save(self,Multiple=False):
        save=True
        if "".join(self.questionTypingBox.getLines()) != " ":
            for box in self.typingBoxes[1:]:
                if Multiple:
                    if len("".join(box.getLines())) > 3:
                        save = save and True
                    else:
                        save = save and False
                else:
                    if len("".join(box.getLines())) > 1:
                        save = save and True
                    else:
                        save = save and False
        else:
            save = False
        if save:
            self.question.questionText = "".join(self.questionTypingBox.getLines())

        return save

    def show(self, win):
        self.questionTypingBox.rect[1] = self.rect[1]
        self.updateHeight()
        for box in self.typingBoxes:
            box.show(win)
        for button in self.buttons:
            button.show(win)

    def isOver(self, mp) -> TypingBox:
        for button in self.buttons:
            button.isOver(mp)

        selBox = None
        for box in self.typingBoxes:
            if box.isOver(mp):
                selBox = box
        return selBox

    def checkButtonClick(self, mp):
        for button in self.buttons.keys():
            if button.isOver(mp):
                self.buttons[button]()

    def reset(self):
        self.question.questionText = ""
        self.genBoxes(new=True)

class MultipleChoiceLayout(Layout):

    def __init__(self, question, rect, editing=False):
        self.optionsBoxes = list() # init in self.genBoxes()
        super().__init__(question, rect)
        # super calls self.genBoxes()

    def genBoxes(self, new=False):
        super().genBoxes(new)
        self.optionsBoxes = list() # reset list
        rect = self.rect[:3] + [10] #10 can be any number, it changes based on font automatically (height)
        rect[0] += rect[2]//20 # add indent
        rect[2] -= rect[2]//20 # equalize width with question box
        firstCharVal = ord("a")
        # the initialize loop doesn't take care of y-values, self.orderBoxes() does that
        for num, optionText in enumerate(self.question.options):
            if new:
                char = chr(firstCharVal + num)  # a, b, c, d...
                optionText = char + "." + optionText
            box = Button_Class.TypingBox(rect=rect.copy(), initText=optionText, bckspcLim=2)
            self.typingBoxes.append(box)
            self.optionsBoxes.append(box)
        self.orderBoxes(self.optionsBoxes, self.questionTypingBox.rect)

    def genButtons(self):
        super().genButtons()
        rect = self.rect[:2] + [20, 20]
        rect[0] -= 20
        rect[1] += self.questionTypingBox.rect[3]
        button = Button_Class.Button(rect, text="+", fontSize=15)
        self.buttons[button] = self.addOption

        rect = rect.copy()
        rect[1] += rect[3]
        button = Button_Class.Button(rect, text="-", fontSize=15)
        self.buttons[button] = self.removeOption

    def addOption(self):

        self.question.options.append("")
        rect = self.optionsBoxes[0].rect.copy()
        box = Button_Class.TypingBox(rect=rect, initText=chr(ord("a")+len(self.optionsBoxes)) + ".", bckspcLim=2)
        self.optionsBoxes.append(box)
        self.typingBoxes.append(box)

    def removeOption(self):
        if len(self.question.options) > 2:
            self.question.options.pop()
            self.optionsBoxes.pop()
            self.typingBoxes.pop()

    def save(self):
        save = super().save(Multiple=True)
        if save:
            arr = list()
            for optionBox in self.optionsBoxes:
                arr.append("".join(optionBox.getLines()))
            self.question.options = arr
        return save

    def show(self, win):
        self.orderBoxes(self.optionsBoxes, self.questionTypingBox.rect)
        self.orderBoxes(self.buttons, self.questionTypingBox.rect)
        super().show(win)

    def reset(self):
        self.question.options = ["",""]
        super().reset()

    def updateHeight(self):
        self.rect[3] = self.optionsBoxes[-1].rect[1] + self.optionsBoxes[-1].rect[3] - self.rect[1] + 100

class NormalQuestionLayout(Layout):

    def __init__(self, question, rect, editing=False):
        super().__init__(question, rect, editing)

class FITBQuestionLayout(Layout):

    def __init__(self, question, rect, editing=False):
        wordBankBox = None # init in self.genBoxes()
        super().__init__(question, rect, editing)

    def genBoxes(self, new=False):
        super().genBoxes(new)

    def genButtons(self):
        super().genButtons()
        rect = self.rect[:2] + [20, 20]
        rect[0] -= 20
        rect[1] += self.questionTypingBox.rect[3]
        button = Button_Class.Button(rect, text="+")
        self.buttons[button] = self.addBlank


    def addBlank(self):
        self.questionTypingBox.words.append(" _____ ")
        self.questionTypingBox.words.append("")

    def show(self, win):
        self.orderBoxes(self.buttons, self.questionTypingBox.rect)
        super().show(win)


class ConnectingQuestionLayout(Layout):
    def __init__(self, question, rect, editing=False):
        self.rColumn = list()
        self.lColumn = list()
        super().__init__(question, rect, editing)

    def genBoxes(self, new=False):
        super().genBoxes(new)
        self.rColumn = list()
        self.lColumn = list()
        rectL = self.rect.copy()[:3] + [10]
        rectL[2] /= 3

        rectR = rectL.copy()
        rectR[0] += self.rect[2] - rectR[2]

        firstCharVal = ord("a")
        # the initialize loop doesn't take care of y-values, self.orderBoxes() does that
        for num in range(len(self.question.lst1)):
            connectionText = self.question.lst1[num]
            if new:
                char = chr(firstCharVal + num)  # a, b, c, d...
                connectionText = char + "." + connectionText
            box = Button_Class.TypingBox(rect=rectL.copy(), initText=connectionText, bckspcLim=2)
            self.typingBoxes.append(box)
            self.lColumn.append(box)

            connectionText = self.question.lst2[num]
            if new:
                num += 1
                connectionText = str(num) + "." + connectionText
            box = Button_Class.TypingBox(rect=rectR.copy(), initText=connectionText, bckspcLim=2)
            self.typingBoxes.append(box)
            self.rColumn.append(box)

        self.orderBoxes(self.rColumn, self.questionTypingBox.rect)
        self.orderBoxes(self.lColumn, self.questionTypingBox.rect)


    def genButtons(self):
        super().genButtons()
        rect = self.rect[:2] + [20, 20]
        rect[0] -= 20
        rect[1] += self.questionTypingBox.rect[3]
        button = Button_Class.Button(rect, text="+", fontSize=15)
        self.buttons[button] = self.addRow

        rect = rect.copy()
        rect[1] += rect[3]
        button = Button_Class.Button(rect, text="-", fontSize=15)
        self.buttons[button] = self.removeRow

    def addRow(self):

        self.question.lst1.append("")
        rect = self.lColumn[0].rect.copy()
        box = Button_Class.TypingBox(rect=rect, initText=chr(ord("a")+len(self.lColumn)) + ".", bckspcLim=2)
        self.lColumn.append(box)
        self.typingBoxes.append(box)

        self.question.lst2.append("")
        rect = self.rColumn[0].rect.copy()
        box = Button_Class.TypingBox(rect=rect, initText=str(1 + len(self.rColumn)) + ".", bckspcLim=2)
        self.rColumn.append(box)
        self.typingBoxes.append(box)

    def removeRow(self):
        if len(self.question.lst1) > 2:
            self.question.lst1.pop()
            self.question.lst2.pop()
            self.rColumn.pop()
            self.lColumn.pop()
            self.typingBoxes.pop()
            self.typingBoxes.pop()


    def reset(self):
        self.question.lst1 = ["",""]
        self.question.lst2 = ["",""]
        super().reset()

    def save(self):
        save = super().save(Multiple=True)
        if save:
            arrR = list()
            arrL = list()
            for i in range(len(self.rColumn)):
                arrR.append("".join(self.rColumn[i].getLines()))
                arrL.append("".join(self.lColumn[i].getLines()))
            self.question.lst1 = arrR
            self.question.lst2 = arrL
        return save

    def show(self, win):
        self.orderBoxes(self.lColumn, self.questionTypingBox.rect)
        self.orderBoxes(self.rColumn, self.questionTypingBox.rect)
        super().show(win)

    def updateHeight(self):
        self.rect[3] = self.rColumn[-1].rect[1] + self.rColumn[-1].rect[3] - self.rect[1] + 100


class TrueFalseLayout(Layout):
    def __init__(self, question, rect, editing=False):
        super().__init__(question, rect, editing)

    def show(self, win):
        self.questionTypingBox.rect[1] = self.rect[1]
        self.questionTypingBox.show(win, extra=" (True/False)")


class OrderingLayout(Layout):

    def __init__(self, MCQuestion, rect, editing=False):
        self.optionsBoxes = list() # init in self.genBoxes()
        super().__init__(question = MCQuestion, rect = rect)
        # super calls self.genBoxes()

    def genBoxes(self, new=False):
        if new:
            self.question.questionText = " Place the following in proper order:"
        super().genBoxes(new)
        self.optionsBoxes = list() # reset list
        rect = self.rect[:3] + [10] #10 can be any number, it changes based on font automatically (height)
        rect[0] += rect[2]//20 # add indent
        rect[2] -= rect[2]//20 # equalize width with question box
        # the initialize loop doesn't take care of y-values, self.orderBoxes() does that
        for num, optionText in enumerate(self.question.options):
            if new:
                optionText = str(num+1) + "." + optionText
            box = Button_Class.TypingBox(rect=rect.copy(), initText=optionText, bckspcLim=2)
            self.typingBoxes.append(box)
            self.optionsBoxes.append(box)
        self.orderBoxes(self.optionsBoxes, self.questionTypingBox.rect)

    def genButtons(self):
        super().genButtons()
        rect = self.rect[:2] + [20, 20]
        rect[0] -= 20
        rect[1] += self.questionTypingBox.rect[3]
        button = Button_Class.Button(rect, text="+", fontSize=15)
        self.buttons[button] = self.addOption

        rect = rect.copy()
        rect[1] += rect[3]
        button = Button_Class.Button(rect, text="-", fontSize=15)
        self.buttons[button] = self.removeOption

        rect = rect.copy()
        rect[1] += rect[3]
        rect[2] = 75
        rect[0] -= rect[2] - 20
        button = Button_Class.Button(rect, text="Shuffle", fontSize=15)
        self.buttons[button] = self.shuffle

    def addOption(self):

        self.question.options.append("")
        rect = self.optionsBoxes[0].rect.copy()
        box = Button_Class.TypingBox(rect=rect, initText=str(len(self.optionsBoxes)+1) + ".")
        self.optionsBoxes.append(box)
        self.typingBoxes.append(box)

    def removeOption(self):

        if len(self.question.options) > 2:
            self.question.options.pop()
            self.optionsBoxes.pop()
            self.typingBoxes.pop()

    def shuffle(self):
        arr = list()
        while self.optionsBoxes:
            ind = random.randint(0,len(self.optionsBoxes)-1)
            arr.append(self.optionsBoxes.pop(ind))
        self.optionsBoxes = arr

    def save(self):
        save = super().save()
        if save:
            arr = list()
            for optionBox in self.optionsBoxes:
                arr.append("".join(optionBox.getLines()))
            self.question.options = arr
        return save

    def show(self, win):
        self.orderBoxes(self.optionsBoxes, self.questionTypingBox.rect)
        self.orderBoxes(self.buttons, self.questionTypingBox.rect)
        super().show(win)

    def reset(self):
        self.question.options = ["",""]
        super().reset()

    def updateHeight(self):
        self.rect[3] = self.optionsBoxes[-1].rect[1] + self.optionsBoxes[-1].rect[3] - self.rect[1] + 100
