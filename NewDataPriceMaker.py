import os
from datetime import datetime
import random

path = "/raw_csvs"
pathFinal = "/final_csvs/"
path_historical = "Historical"
path_shalebasin = "Shale"
path_totlaus = "Total"
numberOfDays = 348
stableRange = 5.0
mediumRange = 10.0
spikeRange = 20.0
#dsDistanceSmall = 15.0
dsDistanceLarge = 20.0
for filename in os.listdir(os.getcwd() + path):
	print("\n\n" + filename)
	
	if path_historical in filename:
		numberOfDays = 348
	else:
		numberOfDays = 260
		
	# read csv file to list
	with open(os.getcwd() + path + "/" + filename , "r") as f:
		
		lst = []
		finalList = []
		maxDelta = 0.0
		maxTotal = 0.0
		minTotal = 10000.0
		for i, line in enumerate(f):
			line = line.split(",")
			item = (line[0].strip() , float(line[1].strip()) )
			lst.append(item)
			if i!=0 and abs(lst[i-1][1] - lst[i][1]) > maxDelta:
				maxDelta = abs(lst[i-1][1] - lst[i][1])
			if lst[i][1] > maxTotal:
				maxTotal = lst[i][1]
			if lst[i][1] < minTotal:
				minTotal = lst[i][1]
				
		# sorting by date
		print(maxDelta)
		date = lst[0]
		date = date[0]
		if(date[1] == '/'):
			lst = sorted(lst, key=lambda x: datetime.strptime(x[0], "%m/%d/%Y"))
		else:
			lst = sorted(lst, key=lambda x: datetime.strptime(x[0], "%Y/%m/%d"))
		
		
		lastTuple = lst[0]
		tempList = []
		
		# removing data by the same day and more than 3 ocurrances
		for index, item in enumerate(lst):
			if item[0] == lastTuple[0]:
				tempList.append(item)
			else:
				if(len(tempList) <= 3):
					for tmpItem in tempList:
						finalList.append(tmpItem)
				else:
					finalList.append(tempList[0])
					finalList.append(tempList[-1])
				lastTuple = item	
				tempList = []
				tempList.append(lastTuple)
				
			if(len(finalList) + len(lst[index:])) <= numberOfDays:
				finalList = finalList + lst[index:]
				break;
		
		# removing middle element of all three ocurrances
		if(len(finalList) > numberOfDays):
			print("second part")
			lst = finalList
			finalList =[]
			lastTuple = lst[0]
			tempList = []
			
			for index,item in enumerate(lst):
				if item[0] == lastTuple[0]:
					tempList.append(item)
				else:
					if(len(tempList) < 3):
						for tmpItem in tempList:
							finalList.append(tmpItem)
					else:
						finalList.append(tempList[0])
						finalList.append(tempList[-1])
					lastTuple = item
					tempList = []
					tempList.append(lastTuple)
				
				if (len(finalList) + len(lst[index:])) <= numberOfDays:
					finalList = finalList + lst[index:]
					break
		
		# removing consecutive data with difference less than 1/15 of max delta
		
		if(len(finalList) > numberOfDays):
			print("third part")
			lst = finalList
			finalList = []
			lastTuple = lst[0]
			tempList = []
			finalList.append(lastTuple)
			
			for index, item in enumerate(lst):
				if item[1] - lastTuple[1] > maxDelta / 15.0:
					finalList.append(item)
				lastTuple = item
				
				if(len(finalList) + len(lst[index:])) <= numberOfDays:
					finalList = finalList + lst[index:]
					break;
		
		print("{0}---->>>     befor : {1}   after : {2}".format(filename, len(lst), len(finalList)))
		
		'''
		# finding maximum and mininum of hub price
		lst = finalList 
		finalList = []
		newTuple = ()
		demand = 0.0
		demandMin = 10000.0
		demandMax = 0.0
		supply = 0.0
		supplyMin = 10000.0
		supplyMax = 0.0
		delta = 0.0
		offset = 0.0
		for index , item in enumerate (lst):
			if index != 0:
				delta = abs(lst[index][1] - lst[index-1][1])
				
			# large chart
			demand = item[1] + dsDistanceLarge
			if 3.0 * delta < maxDelta :
				offset = stableRange
			elif 1.5 * offset < maxDelta:
				offset = mediumRange
			else:
				offset = spikeRange
			if demand < offset * 2.0:
				offset = demand / 2.0
			demandMin = demand - offset
			demandMax = demand + offset
			
			supply = item[1] - dsDistanceLarge
			if supply < 0.0:
				supply = item[1] / 2.0
			if 3.0 * delta < maxDelta :
				offset = stableRange
			elif 1.5 * offset < maxDelta:
				offset = mediumRange
			else:
				offset = spikeRange
			if supply < offset * 2.0:
				offset = supply / 2.0
			supplyMin = supply - offset
			supplyMax = supply + offset

			
			newTuple = (item[0] , item[1], supplyMin, supply, supplyMax, demandMin, demand, demandMax)
			finalList.append(newTuple)
			'''
		
		
		with open(os.getcwd() + pathFinal + filename[:-4] + "_new.csv" , "w") as ff:
			ff.write("day, rigs\n")
			for index, item in enumerate(finalList):
				ff.write("{0}, {1}\n".format(index+1, item[1]))
			
			
		
		
		
'''		
for filename in os.listdir(os.getcwd() + path):
	print("\n\n" + filename)
	
	if filename == "Algonquin Citygate (non-G).csv":
		numberOfDays = 183
	else:
		numberOfDays = 365
		
	# read csv file to list
	with open(os.getcwd() + path + "/" + filename , "r") as f:
		lst = []
		finalList = []
		maxDelta = 0.0
		maxTotal = 0.0
		minTotal = 100.0
		for i, line in enumerate(f):
			line = line.split(",")
			item = (line[0].strip() , float(line[1].strip()) )
			lst.append(item)
			if i!=0 and abs(lst[i-1][1] - lst[i][1]) > maxDelta:
				maxDelta = abs(lst[i-1][1] - lst[i][1])
			if lst[i][1] > maxTotal:
				maxTotal = lst[i][1]
			if lst[i][1] < minTotal:
				minTotal = lst[i][1]
				
		# sorting by date
		print(maxDelta)
		date = lst[0]
		date = date[0]
		if(date[1] == '/'):
			lst = sorted(lst, key=lambda x: datetime.strptime(x[0], "%m/%d/%Y"))
		else:
			lst = sorted(lst, key=lambda x: datetime.strptime(x[0], "%Y/%m/%d"))
		
		
		lastTuple = lst[0]
		tempList = []
		
		# removing data by the same day and more than 3 ocurrances
		for index, item in enumerate(lst):
			if item[0] == lastTuple[0]:
				tempList.append(item)
			else:
				if(len(tempList) <= 3):
					for tmpItem in tempList:
						finalList.append(tmpItem)
				else:
					finalList.append(tempList[0])
					finalList.append(tempList[-1])
				lastTuple = item	
				tempList = []
				tempList.append(lastTuple)
				
			if(len(finalList) + len(lst[index:])) <= numberOfDays:
				finalList = finalList + lst[index:]
				break;
		
		# removing middle element of all three ocurrances
		if(len(finalList) > numberOfDays):
			print("second part")
			lst = finalList
			finalList =[]
			lastTuple = lst[0]
			tempList = []
			
			for index,item in enumerate(lst):
				if item[0] == lastTuple[0]:
					tempList.append(item)
				else:
					if(len(tempList) < 3):
						for tmpItem in tempList:
							finalList.append(tmpItem)
					else:
						finalList.append(tempList[0])
						finalList.append(tempList[-1])
					lastTuple = item
					tempList = []
					tempList.append(lastTuple)
				
				if (len(finalList) + len(lst[index:])) <= numberOfDays:
					finalList = finalList + lst[index:]
					break
		
		# removing consecutive data with difference less than 1/15 of max delta
		
		if(len(finalList) > numberOfDays):
			print("third part")
			lst = finalList
			finalList = []
			lastTuple = lst[0]
			tempList = []
			finalList.append(lastTuple)
			
			for index, item in enumerate(lst):
				if item[1] - lastTuple[1] > maxDelta / 15.0:
					finalList.append(item)
				lastTuple = item
				
				if(len(finalList) + len(lst[index:])) <= numberOfDays:
					finalList = finalList + lst[index:]
					break;
		
		print("{0}---->>>     befor : {1}   after : {2}".format(filename, len(lst), len(finalList)))
		
		
		# finding maximum and mininum of hub price
		lst = finalList 
		finalList = []
		newTuple = ()
		demand = 0.0
		demandMin = 100.0
		demandMax = 0.0
		supply = 0.0
		supplyMin = 100.0
		supplyMax = 0.0
		delta = 0.0
		offset = 0.0
		for index , item in enumerate (lst):
			if index != 0:
				delta = abs(lst[index][1] - lst[index-1][1])
			
			if maxTotal - minTotal > 4.0:
				# large chart
				demand = item[1] + dsDistanceLarge
				if 3.0 * delta < maxDelta :
					offset = stableRange
				elif 1.5 * offset < maxDelta:
					offset = mediumRange
				else:
					offset = spikeRange
				if demand < offset * 2.0:
					offset = demand / 2.0
				demandMin = demand - offset
				demandMax = demand + offset
				
				supply = item[1] - dsDistanceLarge
				if supply < 0.0:
					supply = item[1] / 2.0
				if 3.0 * delta < maxDelta :
					offset = stableRange
				elif 1.5 * offset < maxDelta:
					offset = mediumRange
				else:
					offset = spikeRange
				if supply < offset * 2.0:
					offset = supply / 2.0
				supplyMin = supply - offset
				supplyMax = supply + offset
			else:
				# small chart
				demand = item[1] + dsDistanceSmall
				if 3.0 * delta < maxDelta :
					offset = stableRange
				elif 1.5 * offset < maxDelta:
					offset = mediumRange
				else:
					offset = spikeRange
				if demand < offset * 2.0:
					offset = demand / 2.0
				demandMin = demand - offset
				demandMax = demand + offset
				
				supply = item[1] - dsDistanceSmall
				if supply < 0.0:
					supply = item[1] / 2.0
				if 3.0 * delta < maxDelta :
					offset = stableRange
				elif 1.5 * offset < maxDelta:
					offset = mediumRange
				else:
					offset = spikeRange
				if supply < offset * 2.0:
					offset = supply / 2.0
				supplyMin = supply - offset
				supplyMax = supply + offset
			
			newTuple = (item[0] , item[1], supplyMin, supply, supplyMax, demandMin, demand, demandMax)
			finalList.append(newTuple)
			
		
		
		with open(os.getcwd() + pathFinal + filename[:-4] + "_new.csv" , "w") as ff:
			ff.write("day, hub, supply_min, supply_average, supply_max, demand_min, demand_average, demand_max\n")
			for index, item in enumerate(finalList):
				ff.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}\n".format(index+1, item[1], item[2], item[3], item[4], item[5], item[6], item[7]))
'''