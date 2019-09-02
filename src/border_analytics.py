#!/usr/bin/python3.7
import csv
import os
import sys
from datetime import datetime
from operator import itemgetter, attrgetter
import math

# Create dictionary to hold the data
valDic = {}

# Read data into dictionary
with open(sys.argv[1], "r",) as inputfile:
	readcsv = csv.reader(inputfile, delimiter = ',')	
	next(readcsv)
	for line in readcsv:
		key = line[3] + line[4] + line[5]
		border = line[3]
		date = line[4]
		measure = line[5]
		value = int(line[6])
		if key in valDic:
			valDic[key][3] += value
		else:
			valDic[key] = [border, date, measure, value, 0, 0] # 0s are placeholder for running sum and itemCount
	inputfile.close()  

# Calculate running sum
# Save the parsed time obj into dictionary to avoid redundant recalculation
timeDic = {}
for key in valDic:
	timeDic[key] = datetime.strptime(valDic[key][1], '%m/%d/%Y %I:%M:%S %p')

for key in valDic:
	for key1 in valDic:
		if key != key1:
			day1 = timeDic[key]
			day2 = timeDic[key1]
			if day1 > day2 and valDic[key][2] == valDic[key1][2]:
				valDic[key][4] += valDic[key1][3]
				valDic[key][5] += 1

newcsvfile = []
for key in valDic:
	if valDic[key][5] != 0:
		newcsvfile.append([valDic[key][0], valDic[key][1], valDic[key][2], valDic[key][3], math.ceil(valDic[key][4] / valDic[key][5])])
	else:
		newcsvfile.append([valDic[key][0], valDic[key][1], valDic[key][2], valDic[key][3], 0])
		
newcsvfile = sorted(newcsvfile, key = itemgetter(1,3,2,0), reverse = True)
newcsvfile = [["Border", "Date", "Measure", "Value", "Average"]] + newcsvfile

with open(sys.argv[2], "w") as outputfile:
	writer = csv.writer(outputfile)
	writer.writerows(newcsvfile)    	
		