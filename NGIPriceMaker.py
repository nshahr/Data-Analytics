import os
from datetime import datetime
import random

path = "/raw_csvs"
pathFinal = "/final_csvs/"
numberOfDays = 365
stableRange = 0.04
mediumRange = 0.06
spikeRange = 0.08
dsDistanceSmall = 0.05
dsDistanceLarge = 0.1
WAD = [0.13 , 0.26 , 0.39 , 0.44 , 0.57 ] # WADistance : Weighted Average Distance from hub price
MMD = [0.08 , 0.16 , 0.24 , 0.32 , 0.4 ] # MinMaxDistance : Supply or Demand Minimum and Maximum Distance from Supply or Demand Weighted Average
DF = [1.5 , 2.0 , 2.5 , 3.0 ] # DeltaCoef : Delta Coeficient according to maximum delta
DFR = [1.2 , 1.1 , 0.9 , 0.8] # DeltaCoefReverse : makes small delta's a little bigger and big delta's a little smaller

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
		maxDelta = 0.0	# maximum difference between two consecutive values
		maxTotal = 0.0	# total maximum of data
		minTotal = 100.0	# total minimum of data
		for i, line in enumerate(f):
			# read data from file, and calculate maxDelta, maxTotal & minTotal
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
		maxDelta = 0.0	# maximum difference between two consecutive values
		maxTotal = 0.0	# total maximum of data
		minTotal = 100.0	# total minimum of data
		for i, item in enumerate(lst):
			if i!=0 and abs(lst[i-1][1] - lst[i][1]) > maxDelta:
				maxDelta = abs(lst[i-1][1] - lst[i][1])
			if lst[i][1] > maxTotal:
				maxTotal = lst[i][1]
			if lst[i][1] < minTotal:
				minTotal = lst[i][1]
		finalList = []
		newTuple = ()
		demandAvg = 0.0
		demandMin = 100.0
		demandMax = 0.0
		supplyAvg = 0.0
		supplyMin = 100.0
		supplyMax = 0.0
		hubMin = 100.0
		hubMax = 0.0
		delta = 0.0
		offset = 0.0
		for index , item in enumerate (lst):
			if index != 0:
				delta = abs(lst[index][1] - lst[index-1][1])
			
			deltaIndex = int(delta / maxDelta * 4.0)
			if delta == maxDelta:
				deltaIndex = 3
			WAIndex = int(lst[index][1] / 3.0)
			
			#print("deltaIndex : {0} delta: {1}  maxDelta:{2}  WAIndex:{3}\n".format(deltaIndex, delta , maxDelta, WAIndex))
			
			WAValue = WAD[WAIndex] * DF[deltaIndex]
			
			# find demand and supply prices seperately
			''' 
			demandAvg = lst[index][1] + WAValue
			supplyAvg = lst[index][1] - WAValue
			
			MMValue = MMD[WAIndex] * DF[deltaIndex]
			if(delta < 0.0):
				print("------> delta: {0}\n".format(MMValue))
			demandMin = demandAvg - MMValue
			demandMax = demandAvg + MMValue
			supplyMin = supplyAvg - MMValue
			supplyMax = supplyAvg + MMValue
			'''
			# find hub min and max price. no supply and demand price calculated.
			hubMax = lst[index][1] + WAValue
			hubMin = lst[index][1] - WAValue
			'''
			demandAvg = 0.0
			demandMin = 0.0
			demandMax = 0.0
			
			supplyAvg = 0.0
			supplyMin = 0.0
			supplyMax = 0.0
			'''
			newTuple = (item[0] , hubMin, item[1], hubMax)
			finalList.append(newTuple)
			
		
		
		with open(os.getcwd() + pathFinal + filename[:-4] + "_new.csv" , "w") as ff:
			ff.write("day, hub_min, hub, hub_max\n")
			for index, item in enumerate(finalList):
				ff.write("{0}, {1}, {2}, {3}\n".format(index+1, item[1], item[2], item[3]))
		