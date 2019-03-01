import json

class Person:
    def __init__(self, email):
        self.email = email
        self.contacts = dict()

    def add_sent_mail(self, to, date):
        if to not in self.contacts:
            self.contacts[to] = [date]
        else:
            if date not in self.contacts[to]:
                self.contacts[to].append(date)

    def __str__(self):
        return self.to_json()

    def to_json(self):
        json_dict = dict()
        json_dict[self.email] = self.contacts
        json_dict = json.dumps(json_dict)
        return json_dict[1:-1]

