class Mail:
    # from to date cc bcc
    def __init__(self, fromAddr, toAddr, date, cc, bcc):
        self.fromAddr = fromAddr
        self.toAddr = toAddr
        self.date = date
        self.cc = cc
        if self.cc is not None:
            self.cc = cc.split(', ')
        self.bcc = bcc
        if self.bcc is not None:
            self.bcc = bcc.split(', ')

        self.combinedTo = self.toAddr
        if self.cc is not None:
            self.combinedTo += self.cc

        if self.bcc is not None:
            self.combinedTo += self.bcc

    def __str__(self):
        string = ""
        for to in self.combinedTo:
            string += "{}\t{} -> {}\n".format(self.date, self.fromAddr, to)
        return string.rstrip()

    def to_kv_pair(self):
        return self.fromAddr, self.combinedTo
