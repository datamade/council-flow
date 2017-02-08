import requests, csv

writer = csv.writer(open('committee_participation.csv', 'w'))

def body_offices():

    offices_url = "http://webapi.legistar.com/v1/chicago/officerecords/"

    page_num = 0
    params = {}
    while page_num == 0 or len(response.json()) == 1000 :
        params['$skip'] = page_num * 1000
        response = requests.get(offices_url, params=params)

        for office in response.json() :
            yield office

        page_num += 1

terms = {}

for office in body_offices():


    alderman = office[u'OfficeRecordFullName']
    committee = office[u'OfficeRecordBodyName']
    start = office[u'OfficeRecordStartDate']
    end = office[u'OfficeRecordEndDate']

    key = (alderman, committee)

    if key not in terms:
        terms[key] = {"start_date":start,"end_date":end}
    
    else:

        old_start = terms[key]["start_date"]
        old_end = terms[key]["end_date"]
        if old_start > start:
            terms[key] = {"start_date":start,"end_date":old_end}
        if old_end < end:
            terms[key] = {"start_date":old_start, "end_date":end}
        else:
            terms[key] = {"start_date":old_start,"end_date":old_end}

for d in terms.items():
    
    writer.writerow(d[])

