class Test_Question():
    def __init__(self,question):
        self.questionText = question

    def writeToFile(self, file, number, question_height=9,option_height=7,end="\n"):
        file.write(question_height, str(number) + ". " + self.questionText[1:] + end)


class MC(Test_Question):
    def __init__(self, questionText, options):
        super().__init__(questionText)
        self.options = options

    def writeToFile(self, file, number,question_height,option_height, end="\n"):
        super().writeToFile(file, number,question_height)
        for option in self.options:
            file.write(option_height,option.rjust(len(option)+3) + end)

class FITB(Test_Question):
    def __init__(self, questionText):
        super().__init__(questionText)


class Ordering(Test_Question):
    def __init__(self, questionText, options):
        self.options = options
        super().__init__(questionText)

    def writeToFile(self, file, number,question_height,option_height, end="\n"):
        super().writeToFile(file, number,question_height)
        for option in self.options:
            file.write(option_height,option.rjust(len(option) + 3) + end)
        for times in range(len(self.options)):
            file.write(option_height,"__ ")
        file.write(option_height,"\n")

class True_False(Test_Question):
    def __init__(self, questionText):
        super().__init__(questionText)

    def writeToFile(self, file, number,question_height,option_height):
        super().writeToFile(file, number, question_height,end="")
        file.write(question_height," (True/False)\n")


class Normal(Test_Question):
    def __init__(self, questionText):
        super().__init__(questionText)


class Connecting(Test_Question):
    def __init__(self, questionText, lst1,lst2):
        super().__init__(questionText)
        self.lst1 = lst1
        self.lst2 = lst2


    def writeToFile(self, file, number,question_height,option_height, end="\n"):
        super().writeToFile(file, number,question_height)
        self.max_chr = max(self.lst2,key=len)
        print(self.lst1)
        print(self.lst2)
        print(self.max_chr)
        self.max_chr=len(self.max_chr)
        for i in range(len(self.lst1)):
            s=3*" "+self.lst2[i]+(self.max_chr-len(self.lst2[i])+3)*" "+self.lst1[i]+end
            print(s)
            file.write(option_height,s)
