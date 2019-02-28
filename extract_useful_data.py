import os
import json
import operator
import json
import pickle
from mail import Mail
from person import Person
from email.parser import BytesParser, Parser
from email.policy import default
from itertools import groupby
from collections import defaultdict
from pprint import pprint

def generate_objects():
    mailList = []
    for subdir, dirs, files in os.walk("maildir"):
        for file in files:
            filepath = subdir + os.sep + file

            with open(filepath, 'rb') as f:
                header = BytesParser(policy=default).parse(f)

            # from to date cc bcc
            if header['from'] is None or header['to'] is None:
                continue

            this_mail = Mail(header['from'], header['to'].split(', '), header['date'], header['cc'], header['bcc'])
            # print(this_mail)
            mailList.append(this_mail)

    with open('mail_data.pkl', 'wb') as output:
        for a_mail in mailList:
            pickle.dump(a_mail, output, pickle.HIGHEST_PROTOCOL)


def pickled_items(filename):
    """ Unpickle a file of pickled data. """
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def load_objects():
    mail_list = [m.to_kv_pair() for m in pickled_items("mail_data.pkl")]
    mail_list.sort(key=operator.itemgetter(0))

    # for person in mail_list:
    #     contacts_dict = dict()
    #     for contacts in person[1]:
    #         if contacts[0] not in contacts_dict:
    #             contacts_dict[contacts[0]] = [contacts[1]]
    #         else:
    #             contacts_dict[contacts[0]].append(contacts[1])
    #     person[1] = contacts_dict
    # for person_key, person in enumerate(mail_list):
    #     d = dict()
    #     for key, value in person:
    #         if key not in d:
    #             d[key] = list(value)
    #         else:
    #             d[key].append(value)
    #     mail_list[person_key][1] = d

    return mail_list


def parse_objects():
    mail_list = load_objects()

    people_list = dict()

    for key, people in groupby(mail_list, lambda x: x[0]):
        # people_list.append(dict(email=key, contacts=list(v[1] for v in people)))
        # result.append(dict(type=key, items=list(v[0] for v in valuesiter)))
        # pprint(list(people))
        for mail_person in people:
            if mail_person[0] not in people_list:
                person = Person(mail_person[0])
                for correspondence in mail_person[1]:
                    person.add_sent_mail(correspondence[0], correspondence[1])
                people_list[key] = person
            else:
                person = people_list[key]
                for correspondence in mail_person[1]:
                    person.add_sent_mail(correspondence[0], correspondence[1])
                people_list[key] = person

    json_string = "var result = {"
    for v in people_list.values():
        json_string += v.to_json() + ','

    json_string += "}"

    print(json_string)
    # [{'type': k, 'items': v} for k, v in res.items()]
    #     for email in group:
    #         if key not in people_list:
    #             people_list[key] = Person(key)
    #         else:
    #             people_list[key].add_sent_mail(email[0], email[1])
    #
    # for person in people_list.values():
    #     print(person.to_json())

    # with open('result.json', 'w') as fp:
    #     json.dump(people_list, fp)


if __name__ == "__main__":
    # generate_objects()
    parse_objects()
    # pprint(load_objects())

