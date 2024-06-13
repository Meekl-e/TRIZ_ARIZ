



class Object:
    def __init__(self,word, svoistva=None, role=None) :

        self.svoistva = svoistva
        self.role = role
        self.word = word
        self.protivorechiya = []


# На заводе стираются детали из-за камней
    def antiSvoistva(self):

        for i in range(len(self.svoistva)):
            if self.svoistva[i].startswith("не"):
                self.svoistva[i] = self.svoistva[i][2:]
            else:
                self.svoistva[i] = "не" + self.svoistva[i]
        return self.svoistva
class Verb:
    def __init__(self,word, goal) :
        self.goal = goal
        self.word = word


