import urllib, json, csv, sys
from datetime import datetime
reload(sys)    
sys.setdefaultencoding('utf-8')

writer = csv.writer(open('attendance.csv', 'w'))
terms = csv.reader(open('committee_terms_clean.csv', 'rU'))
meetings = csv.reader(open('who_there.csv', 'rU'))

meetings_record = {}

for line in meetings:
	c = line[0]
	d = datetime.strptime(line[1] , '%m/%d/%y') 
	a = line[2]
	if c in meetings_record.keys():
		if d in meetings_record[c]:
			meetings_record[c][d][a] = 'present'
		else:
			meetings_record[c][d] = {
				a: 'present'
			}
	else:
		meetings_record[c] = {
			d: {
				a: 'present'
			}
		}

for line in terms:
	ald = line[0]
	comm = line[1]
	st = datetime.strptime(line[2] , '%m/%d/%y')
	en = datetime.strptime(line[3] , '%m/%d/%y')
	for comm in line:
		if comm in meetings_record.keys():
			date = meetings_record[comm].keys()
			for d in date:
				if (d > st) and (d < en):
					attendee = meetings_record[comm][d].keys()
					if ald not in attendee:
						meetings_record[comm][d][ald] = 'absent'


for x in meetings_record.items():
	committee = x[0]
	who_there = x[1]
	for y in who_there.items():
		days = y[0]
		went = y[1]
		for z in went.items():
			people = z[0]
			status = z[1]

			writer.writerow([committee, days, people, status])





