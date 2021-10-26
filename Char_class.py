class character():
    def __init__(self, nick, cls, lv, pos):
        self.nick = nick
        self.cls = cls
        self.lv = lv
        self.pos = pos

    def to_lst(self):
        return [self.nick, self.cls, self.lv, self.pos]

    def __repr__(self):
        return "{} {} {} {}".format(self.nick, self.cls, self.lv, self.pos)

    def __str__(self):
        return [self.nick, self.cls, self.lv, self.pos]