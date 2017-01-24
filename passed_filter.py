import urllib, json, csv, sys
reload(sys)    
sys.setdefaultencoding('utf-8')

page_num = 1
writer = csv.writer(open('passed_clean.csv', 'w'))
search_url = "http://ocd.datamade.us/bills/?from_organization=ocd-organization/ef168607-9135-4177-ad8e-c1f7a4806c3a&actions__description=Passed&legislative_session__identifier=2011&page=%d"
while page_num:
	print page_num
	url = search_url % page_num
	response = urllib.urlopen(url)
	failed_bills_raw = json.loads(response.read())
	if not failed_bills_raw:
    		break
	result = failed_bills_raw[u'results']
	for item in result:
		if u'id' in item and len(item[u'id']) > 0:
			l = item[u'id']
			url2 = "http://ocd.datamade.us/%s/" % l
			bill_info = urllib.urlopen(url2)
			info = json.loads(bill_info.read())
			sponsorship = info[u'sponsorships']
			for x in sponsorship:
				if u'entity_name' in x:
					sponsor = x[u'entity_name']
				else:
					sponsor = []
			writer.writerow([info[u'title'], info[u'identifier'], sponsor, info[u'classification'], info[u'votes']])
		else:			
			continue
	page_num += 1