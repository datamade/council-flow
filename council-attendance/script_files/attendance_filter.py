import urllib, json, csv, sys
reload(sys)    
sys.setdefaultencoding('utf-8')

page_num = 1
writer = csv.writer(open('meeting_attendance.csv', 'w'))
search_url = "http://ocd.datamade.us/events/?jurisdiction=ocd-jurisdiction/country:us/state:il/place:chicago/government&updated_at__gt=2017-02-04&page=%d"

while page_num:
	print page_num
	url = search_url % page_num
	response = urllib.urlopen(url)
	committee_events = json.loads(response.read())
	if not committee_events:
    		break
	results = committee_events[u'results']
	for item in results:
		if u'id' in item and len(item[u'id']) > 0:
			l = item[u'id']
			url2 = "http://ocd.datamade.us/%s/" % l
			event_info = urllib.urlopen(url2)
			info = json.loads(event_info.read())
			happened = info[u'status']
			who_there = info[u'participants']
			if happened == u'confirmed':
				for x in who_there:
					if (u'entity_name' in x) and (x[u'entity_type'] == u'person'):
						attendee = x[u'entity_name']
						writer.writerow([info[u'name'], info[u'start_time'], attendee, info[u'status']])
					else:
						attendee = []
						writer.writerow([info[u'name'], info[u'start_time']])
			else:			
				continue
		else:			
			continue
	page_num += 1