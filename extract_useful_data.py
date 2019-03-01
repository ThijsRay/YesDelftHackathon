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
    return people_list


# def parse_to_simple_graph():
#     people_list = parse_objects()
#
#     node_weights = {}
#
#     edges = {}
#     nodes = []
#
#     for (addr, mails) in people_list.items():
#         if addr not in node_weights:
#             node_weights[addr] = 0
#             for person in mails.contacts:
#                 if person not in node_weights:
#                     node_weights[person] = 0
#                 weight = len(mails.contacts)
#                 node_weights[addr] += weight
#                 node_weights[person] += weight
#                 if addr not in edges:
#                     edges[addr] = [{'from': addr, 'to': person, 'value': weight, 'url': "timeline.html?from={}&to={}".format(addr, person)}]
#                 else:
#                     edges[addr].append({'from': addr, 'to': person, 'value': weight, 'url': "timeline.html?from={}&to={}".format(addr, person)})
#             nodes[addr] = [{'id': addr, 'label': addr, 'value': node_weights[addr]}]
#
#     with open("front_end/data/connected_edges.js", 'w') as outfile:
#         outfile.write("let connected_edges = " + json.dumps(edges))
#
#     with open("front_end/data/connected_nodes.js", 'w') as outfile:
#         outfile.write("let connected_nodes= " + json.dumps(nodes))


def parse_to_graph():
    people_list = parse_objects()

    node_weights = {}

    edges = []
    nodes = []

    for (addr, mails) in people_list.items():
        if addr not in node_weights:
            node_weights[addr] = 0
            for person in mails.contacts:
                if person not in node_weights:
                    node_weights[person] = 0
                weight = len(mails.contacts)
                node_weights[addr] += weight
                node_weights[person] += weight
                edges.append({'from': addr, 'to': person, 'value': weight, 'url': "timeline.html?from={}&to={}".format(addr, person)})
            if "@enron" in addr and node_weights[addr] > 0:
                nodes.append({'id': addr, 'label': addr, 'value': node_weights[addr]})

    with open("front_end/data/edges.js", 'w') as outfile:
        outfile.write("let edges = " + json.dumps(edges))

    with open("front_end/data/nodes.js", 'w') as outfile:
        outfile.write("let nodes = " + json.dumps(nodes))

    # function parseData(data) {
    #   var map = new Map();
    #   for (var key in data) {
    #     var email = data[key].e;
    #     if (!map.has(email)) {
    #       map.set(email, 0);
    #     }
    #     var mails = data[key].c;
    #     for (var person in mails) {
    #       // console.log(mails[person]);
    #       if (!map.has(person)) {
    #         map.set(person, 0);
    #       }
    #       dates = mails[person];
    #       addWeight(map, key, person, dates.length);
    #       edges.add({
    #         from: email,
    #         to: person,
    #         value: dates.length
    #       });
    #     }
    #   }
    #   map.forEach(createNode);
    # }

#
# function
# createNode(value, key, map)
# {
#     nodes.add({
#         id: key,
#         label: key,
#         value: value
#     });
# }
# function
# addWeight(map,
# from, to, weight) {
#     map.set(
# from, map.get(
# from) + weight);
# map.set(to, map.get(to) + weight);
# }

def generate_result_json():
    json_string = "let result = {"
    for v in parse_objects().values():
        json_string += v.to_json() + ','
    json_string = json_string[:-1]
    json_string += "}"

    with open("front_end/data/result.js", 'w') as outfile:
        outfile.write(json_string)


if __name__ == "__main__":
    # generate_objects()
    parse_objects()
    parse_to_graph()
    # parse_to_simple_graph()
    generate_result_json()
    # pprint(load_objects())

