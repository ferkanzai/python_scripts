import re

regex = 'REPORT'
total = 0
count = 0
abv_30 = 0
blw_30 = 0
count_blw = 0

with open('C:\\Users\\fca\\AppData\\Local\\Temp\\lambda_logs_after.txt', 'r') as file:
	for line in file:
		if re.search(regex, line):
            time = float(re.findall('  Duration: ([0-9]+\.[0-9]+)'))
			#words = line.split()
			#time = float(words[4])
			#print(time)
			total += time
			if time >= 30000:
				abv_30 += 1
			else:
				blw_30 += time
				count_blw += 1
			count += 1

avg = total / count
print("Total: " , count)
print("Media: ", avg)
print("Above 30: ", abv_30)
print("Media no timeout: ", (blw_30 / count_blw))