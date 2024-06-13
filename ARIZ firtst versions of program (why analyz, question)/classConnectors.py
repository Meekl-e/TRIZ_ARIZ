



class Connector:
    def __init__(self, typeObject, word=None, verb=None, mainWord=None):
        # typeObject
        # False - с нет
        # True - с да
        # None - задача
        self.typeO = typeObject

        self.word = word
        self.verbConnect = verb
        self.mainWord = mainWord

