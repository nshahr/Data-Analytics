import os
from datetime import datetime
import random
import re

path = "/Final_Result_For_Anylogic"

allhubsdata = []
hubnames = []
counter = 0
filecounter = -1
with open(os.getcwd() + "/" + "database2.csv"  , "w" ) as ff:
	titles = "day, name, id, report\n"
	ff.write(titles)
	for  filename in os.listdir(os.getcwd() + path):
		print("\n\n" + filename)
		colName = filename[0:-8]
		colName = re.sub(r"[^\w\s]", '' , colName)
		colName = colName.replace(" " , "_")
		colName = colName.lower()
		hubnames.append(colName)
		print(colName)
		counter = 0
		filecounter += 1
		with open(os.getcwd() + path + "/" + filename , "r") as f:
			hubdata = []
			for i, line in enumerate(f):
				if i == 0:
					continue
				counter +=1
				line = line.split(",")
				tempstring = "{" + line[1].strip() + "," + line[2].strip() + "," + line[3].strip() + "}"
				finalstr = '{0},{1},{2},"{3}"\n'.format(i, colName, filecounter, tempstring)
				ff.write(finalstr)
				hubdata.append(tempstring)
				#print(tempstring)
		
			print(counter)
		allhubsdata.append(hubdata)
'''	
daycount = len(allhubsdata[0])
print(daycount)

with open(os.getcwd() + "/" + "database.csv"  , "w" ) as ff:
	titles = "day, "
	for i , name in enumerate(hubnames):
		titles += name + ", "
	titles += "\n"
	ff.write(titles)

	for i in range(0,daycount):	
		print(i)
		line = "{0},".format(i)
		for j , lst in enumerate(allhubsdata):
			line += '"{0}"'.format(lst[i])
			if j != len(allhubsdata) - 1:
				line += ","
		line += "\n"
		ff.write(line)
'''	