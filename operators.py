class elements(object):
    def __init__(self, other, blank, player):
        self._player = player
        self._other = other
        self._blank = blank

    def iGoWins(self):
        if self._player == 2 and self._blank == 1:
            return True
        else:
            return False

    def otherGoWins(self):
        if self._other == 2 and self._blank == 1:
            return True
        else:
            return False
