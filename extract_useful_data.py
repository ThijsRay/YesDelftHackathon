import os
import json
import operator
import pickle
import json
from mail import Mail
from email.parser import BytesParser, Parser
from email.policy import default
from itertools import groupby

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
    mailList = [m.to_kv_pair() for m in pickled_items("mail_data.pkl")]
    mailList.sort(key=operator.itemgetter(0))
    return mailList


def parse_objects():
    mailList = load_objects()

    dictList = dict()

    for key, group in groupby(mailList, lambda x: x[0]):
        for x in group:
            if key not in dictList:
                dictList[key] = list()
            for to in x[1]:
                dictList[key].append(to)

    with open('result.json', 'w') as fp:
        json.dump(dictList, fp)

if __name__ == "__main__":
    # generate_objects()
    parse_objects()

