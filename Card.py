class Card(object):
    def __init__(self,value,suit, fullValue, intValue, fullSuit):
        self.value=value
        self.suit=suit
        self.fullValue=fullValue
        self.intValue=intValue
        self.fullSuit=fullSuit

    def showFull(self):
        print("{} of {}".format(self.fullValue,self.fullSuit))

    def showMini(self):
        print("{}{}".format(self.value,self.suit))