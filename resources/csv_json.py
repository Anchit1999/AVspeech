import sys
import csv, json
from collections import OrderedDict

data = {}
classes = []
with open(sys.argv[1]) as csvFile:
	csvReader = csv.DictReader(csvFile)
	for rows in csvReader:
		yid = rows['id']
		if yid in data:
			data[yid]['annotations']['segment'].append([float(rows['start']),float(rows['end'])])
			data[yid]['annotations']['center'].append([float(rows['x']),float(rows['y'])])
		else:
			classes.append(yid)
			data[yid] = OrderedDict()
			data[yid]['annotations'] = OrderedDict()
			data[yid]['annotations']['segment'] = []
			data[yid]['annotations']['segment'].append([float(rows['start']),float(rows['end'])])
			data[yid]['annotations']['center'] = []
			data[yid]['annotations']['center'].append([float(rows['x']),float(rows['y'])])

		data[yid]['url'] = "https://www.youtube.com/watch?v=" + rows['id']


with open(sys.argv[2],'w') as jsonFile:
	jsonFile.write(json.dumps(data,indent=4))

with open('yids.json','w') as jsonFile:
	jsonFile.write(json.dumps(classes,indent=4))