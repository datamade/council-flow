import urllib.request
import json
import codecs

BASE_URL = 'http://ocd.datamade.us/{}'
UNICODE_READER = codecs.getreader("utf-8")

def bill_pages(base_url) :

    page = 1
    while True :
        with urllib.request.urlopen(base_url.format(page)) as bills_page :
            bills = json.load(UNICODE_READER(bills_page))
            yield bills['results']
            if bills['meta']['page'] < bills['meta']['max_page'] :
                page += 1
            else :
                break

def actions(base_url) :
    for bill_page in bill_pages(base_url) :
        for bill in bill_page :
            with urllib.request.urlopen(BASE_URL.format(bill['id'])) as bp :
                bill = json.load(UNICODE_READER(bp))
                yield bill['actions']


base_bill_page = 'http://ocd.datamade.us/bills/?from_organization=ocd-organization/ef168607-9135-4177-ad8e-c1f7a4806c3a&page={}'


def action_graph(sequence, graph) :
    event, *sequence = sequence
    if event not in graph :
        graph[event]= {'counter' : 0, 'children' : {}}

    if sequence :
        children = graph[event]['children']
        graph[event]['children'].update(action_graph(sequence, children))

    graph[event]['counter'] += 1

    return graph



graph = {}

for i, bill_actions in enumerate(actions(base_bill_page)) :
    if bill_actions :
        graph = action_graph([act['description'] for act in bill_actions], graph)

with open('flow.json', 'w') as outfile :
    json.dump(graph, outfile, sort_keys=True, indent=4)

