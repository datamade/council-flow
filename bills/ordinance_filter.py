import urllib, json, csv
url = "http://ocd.datamade.us/bills/?from_organization=ocd-organization/ef168607-9135-4177-ad8e-c1f7a4806c3a"
response = urllib.urlopen(url)
bills_raw = json.loads(response.read())
results = bills_raw[u'results']
writer = csv.writer(open("bills_clean.csv", 'wb'))
for item in results:
	if u'classification' in item and item[u'classification'] == [u'ordinance']:
		writer.writerow([item[u'title']])
		writer.writerow([item[u'identifier']])
	else:
		continue