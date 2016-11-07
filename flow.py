import requests
import json

BASE_URL = 'http://ocd.datamade.us/{}'

session = requests.Session()

def bill_pages(base_url) :
    page = 1
    while True :
        response = session.get(base_url.format(page))
        bills = response.json()
                              
        yield bills['results']
        if bills['meta']['page'] < bills['meta']['max_page'] :
            page += 1
        else :
            break

def actions(base_url) :
    for bill_page in bill_pages(base_url) :
        for bill in bill_page :
            response = session.get(BASE_URL.format(bill['id']))
            bill = response.json()
            yield bill['actions']


def action_graph(sequence, graph) :
    event, *sequence = sequence
    if event not in graph :
        graph[event]= {'counter' : 0, 'children' : {}}

    if sequence :
        children = graph[event]['children']
        graph[event]['children'].update(action_graph(sequence, children))

    graph[event]['counter'] += 1

    return graph


if __name__ == '__main__':

    base_bill_page = 'http://ocd.datamade.us/bills/?from_organization=ocd-organization/ef168607-9135-4177-ad8e-c1f7a4806c3a&page={}'

    graph = {}

    for i, bill_actions in enumerate(actions(base_bill_page)) :
        if bill_actions :
            graph = action_graph([act['description'] for act in bill_actions], graph)
        if i % 100 == 0:
            print(i)
            

    with open('flow.json', 'w') as outfile :
        json.dump(graph, outfile, sort_keys=True, indent=4)

