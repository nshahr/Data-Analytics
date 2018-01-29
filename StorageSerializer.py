import os 
from datetime import datetime
import random


statesDic = {'Alabama' : 1023,
'Arizona' : 1012,
'Arkansas' : 1022,
'California' : 1049, 
'Colorado' : 1026,
'Connecticut' : 1016,
'Delaware' : 1006,
'District of Columbia' : 1007,
'Florida' : 1048,
'Georgia' : 1014,
'Idaho' : 1005,
'Illinois' : 1041,
'Indiana' : 1017,
'Iowa' : 1029,
'Kansas' : 1015,
'Kentucky' : 1046,
'Louisiana' : 1031,
'Maine' : 1018,
'Maryland' : 1021,
'Massachusetts' : 1019,
'Michigan' : 1002,
'Minnesota' : 1009,
'Mississippi' : 1039,
'Missouri' : 1003,
'Montana' : 1020,
'Nebraska' : 1025,
'Nevada' : 1011,
'New Hampshire' : 1008,
'New Jersey' : 1042,
'New Mexico' : 1032,
'New York' : 1045,
'North Carolina' : 1004,
'North Dakota' : 1010,
'Ohio' : 1043,
'Oklahoma' : 1028,
'Oregon' : 1040,
'Pennsylvania' : 1034,
'Rhode Island' : 1047,
'South Carolina' : 1035,
'South Dakota' : 1001,
'Tennessee' : 1030,
'Texas' : 1044,
'Utah' : 1036,
'Vermont' : 1027,
'Virginia' : 1024,
'Washington' : 1038,
'West Virginia' : 1037,
'Wisconsin' : 1013,
'Wyoming' : 1033}


statenames = []
yearlist = []
allyearslist = []

with open(os.getcwd() + "/Net Withdrawals - One Cycle.csv", "r") as f:
	for i , line in enumerate(f):
		if i == 0 :
			line = line.split(",")
			for j, name in enumerate(line):
				if j == 0 : continue
				statenames.append(name.strip())
				allyearslist.append([])
		else:
			line = line.split(",")
			for j , temp in enumerate(line):
				if j == 0 : continue
				allyearslist[j-1].append(temp.strip())
				
with open(os.getcwd() + "/storage_monthly_withdrawals.csv" , "w") as resultfile :
	resultfile.write("month, state_name, state_id, withdrawal\n")
	for i , state  in enumerate(statenames):
		for j , month in enumerate(allyearslist[i]):
			row = "{0}, {1}, {2}, {3}\n".format(j+1, statenames[i], statesDic[state], allyearslist[i][j])
			resultfile.write(row)
		print(state)