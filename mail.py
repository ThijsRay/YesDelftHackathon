class Mail:
    def __init__(self):
        self.fromAddr = ""
        self.toAddr = ""
        self.cc = ""
        self.bcc = ""

    def print_mail(self):
        print(self.fromAddr, " -> ", self.toAddr)
