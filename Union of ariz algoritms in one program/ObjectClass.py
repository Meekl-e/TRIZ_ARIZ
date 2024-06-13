



class Object:
    def __init__(self,word, svoistva=None, role=None) :

        self.svoistva = svoistva
        self.role = role
        self.word = word
        self.protivorechiya = []
        self.ASV = []


# На заводе стираются детали из-за камней
    def antiSvoistva(self):

        for i in range(len(self.svoistva)):
            if self.svoistva[i].startswith("не"):
                self.ASV.append(self.svoistva[i][2:])
            else:
                self.ASV.append("не" + self.svoistva[i])
        return self.ASV
