import json


countyList = []
allCountyList = []
finalList = []
def ReadCounties():
	with open("county_list.csv" , "r") as countyfile:
		for i, line in enumerate(countyfile):
			item = line.split(",")
			countyList.append((item[0].strip(), int(item[1].strip()), int(item[2].strip())))
			#print(line.strip())
		#print(countyList)

def ReadAllCounties():		
	with open("states_42_55_39.txt" , "r") as allcountys:
		for i , line in enumerate(allcountys):
			if(len(line.strip()) != 1):
				jsonobject = json.loads(line.strip())
				allCountyList.append(jsonobject)
				print(jsonobject["type"])
				
				#print("*" + line.strip() + "*")
		#print(allCountyList)

def Main():
	counter = 0
	counter2 = 0
	with open("maps.js" , "w") as fixedfile:
		with open("county_codes_file.csv" , "w") as countyFile:
			fixedfile.write("var geoJSONData = {\"type\": \"FeatureCollection\",\"features\": [")
			countyFile.write("[")
			for i, item in enumerate(countyList):
				counter2 += 1
				for j, jsonObject in enumerate(allCountyList):
					tempObject = jsonObject["properties"]
					stateNum = int(tempObject["STATE"])
					if stateNum == 42 : stateNum = 35
					elif stateNum == 54 : stateNum = 45
					elif stateNum == 39 : stateNum = 32
					
					shaleplay = item[2]
					color = "#5f9ea0"
					if shaleplay == 0 :  color = "#5f9ea0"
					if shaleplay == 1 :  color = "#e38989"
					if shaleplay == 2 :  color = "#630367"
					
					print(stateNum)
					if item[0] == tempObject["NAME"] and item[1] == stateNum :
						counter += 1
						tempObject["fill"] = color
						fixedfile.write("{0}".format(json.dumps(jsonObject)))
						countyFile.write("{{ oldcode : {0} , state : {1} , newcode : {2} }}\n".format(int(tempObject["COUNTY"]) , int(tempObject["STATE"]), i))
						
						if i != len(countyList) - 1:
							fixedfile.write(",")
							countyFile.write(",")
			fixedfile.write("]};")
			print(counter)
			print(counter2)
ReadCounties()
ReadAllCounties()	
Main()