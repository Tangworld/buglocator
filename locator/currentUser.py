class CurrentUser:
    b1 = 0
    b2 = 0
    b3 = 0
    b4 = 0
    b5 = 0
    b6 = 0
    b7 = 0
    myall = 0
    othersall = 0

    def setB1(self,b1):
        self.b1 = b1
    def getB1(self):
        return self.b1

    def setB2(self,b2):
        self.b2 = b2
    def getB2(self):
        return self.b2

    def setB3(self,b3):
        self.b3 = b3
    def getB3(self):
        return self.b3

    def setB4(self,b4):
        self.b4 = b4
    def getB4(self):
        return self.b4

    def setB5(self,b5):
        self.b5 = b5
    def getB5(self):
        return self.b5

    def setB6(self,b6):
        self.b6 = b6
    def getB6(self):
        return self.b6

    def setB7(self,b7):
        self.b7 = b7
    def getB7(self):
        return self.b7


    def setAll(self,b1,b2,b3,b4,b5,b6,b7,myall,othersall):
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.b4 = b4
        self.b5 = b5
        self.b6 = b6
        self.b7 = b7
        self.myall = myall
        self.othersall = othersall

    def setB(self,b1,b2,b3,b4,b5,b6,b7):
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.b4 = b4
        self.b5 = b5
        self.b6 = b6
        self.b7 = b7


    def setMyall(self,myall):
        self.myall = myall
    def getMyall(self):
        return self.myall

    def setOthersall(self,othersall):
        self.othersall = othersall
    def getOthersall(self):
        return self.othersall
