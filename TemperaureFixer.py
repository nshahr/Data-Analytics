import os
from datetime import datetime, date, timedelta


path = "/raw_temperatures"
pathFinal = "/final_temperatures/"
numberOfDays = 6205
startDate = date(2000, 1, 1)
endDate = date(2016, 12, 31)
deltaDate = endDate - startDate
csvDic = {}
finalDic = {}

def Main():
	for filename in os.listdir(os.getcwd() + path):
		print("\n\n" + filename)
		
		#read csv files to list
		with open(os.getcwd() + path + "/" + filename , "r") as f:
			lst = []
			maxDelta = 0.0
			maxTotal = -100.0
			minTotal = 200.0
			index = 0
			csvDic = {}
			global finalDic 
			finalDic = {}
			for i, line in enumerate(f):
				if(i != 0):
					line = line.split(",")
					item = (line[2].strip() , float(line[3].strip()), line[1].strip() )
					if index != 0 and lst[index-1][1] > 20.0 and item[1] <= 0.0:
						continue
					lst.append(item)
					if index!=0 and abs(lst[index-1][1] - lst[index][1]) > maxDelta:
						maxDelta = abs(lst[index-1][1] - lst[index][1])
					if lst[index][1] > maxTotal:
						maxTotal = lst[index][1]
					if lst[index][1] < minTotal:
						minTotal = lst[index][1]
					index += 1
					
		mDate = date(2000, 1, 1)
		# format dates to match yyyy-mm-dd
		for index, item in enumerate(lst):
			if "/" in item[0]:
				tempDate = item[0].split("/")
				mDate = str(date(int(tempDate[2]), int(tempDate[0]), int(tempDate[1])))
			else:
				mDate = str(date(int(item[0][:4]), int(item[0][4:6]), int(item[0][6:])))
			csvDic[mDate] = (item[1], item[2])
		
		st = ""
		# fix date sequence over all years
		for i in range(deltaDate.days + 1):
			st += str(startDate + timedelta(days = i))
			currentDate = str(startDate + timedelta(days = i))
			finalDic[currentDate] =  csvDic.get(currentDate , None)
		
		# fill empty spaces between dates with previous and following years data
		for key, value in finalDic.items():
			finalDic[key] = GetProperValue(key)
		
		# write date in file with the same name
		with open(os.getcwd() + pathFinal + filename[:-4] + "_new.csv" , "w") as ff:
			ff.write("day, average_temp, station\n")
			for key, value in finalDic.items():
				if(value != None):
					ff.write("{0}, {1}, {2}\n".format(key, value[0], value[1]))
			
def GetProperValue(currentdate):
	value = finalDic.get(str(currentdate)) 
	if value != None:
		return value
	tempdate = currentdate.split("-")
	# check past years
	for i in range(int(tempdate[0]) - 1, 1999, -1):
		newdate = "" + str(i) + "-" + tempdate[1] + "-" + tempdate[2]
		newvalue = finalDic.get(newdate)
		if newvalue  != None:
			return newvalue
	# check following years
	for i in range(int(tempdate[0]) + 1, 2016):
		newdate = "" + str(i) + "-" + tempdate[1] + "-" + tempdate[2]
		newvalue = finalDic.get(newdate)
		if newvalue  != None:
			return newvalue
			
	print("nooooooooo")
			
	
Main()