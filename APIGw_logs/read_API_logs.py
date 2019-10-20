import os, re, json
from datetime import datetime

path = '/Users/fca/Downloads/testZip'
regex_200 = 'Method completed with status: 200'
regex_403 = 'Method completed with status: 403'
file_list = []
count1 = 0
count2 = 0
later_files = []
time_200 = []
request_id = None

for r, d, f in os.walk(path):
    for fi in f:
        #print(fi)
        new_path = os.path.join(path, fi)
        #print(new_path)
        with open(new_path, 'r') as ff:
            line_count = 0
            for line in ff:
                words = line.split()
                request_id = words[1].strip('()')
                #print(words[0])
                if re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z', words[0]) and re.search(regex_200, line):
                    time = datetime.strptime(words[0], '%Y-%m-%dT%H:%M:%S.%fZ')
                    #print(time.minute)
                    line_count += 1
                    time_200.append([time.hour, time.minute, time.second, time.microsecond])
            if line_count > 0:
                file_list.append({"time": time, "file": ff.name.split('/')[-1], "request ID": request_id})
        count1 += 1

for r, d, f in os.walk(path):
    for fi in f:
        #print(fi)
        new_path = os.path.join(path, fi)
        with open(new_path, 'r') as ff:
            line_count = 0
            for line in ff:
                words = line.split()
                request_id = words[1].strip('()')
                time_403 = []
                #print(words[0])
                if re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z', words[0]) and re.search(regex_403, line):
                    time = datetime.strptime(words[0], '%Y-%m-%dT%H:%M:%S.%fZ')
                    time_403.append([time.hour, time.minute, time.second, time.microsecond])
                    #print(time_403)
                    #print(time.minute)
                    if time_403 > time_200:
                        #later_file.append({"time": time, "file": ff.name.split('/')[-1]})
                        line_count += 1
            if line_count > 0:
                later_files.append({"time": time, "file": ff.name.split('/')[-1], "request ID": request_id})
        count2 += 1

#file_list.sort()
print(json.dumps({"Files with 200 response": file_list}, indent=2, default=str))
print(json.dumps({"Files with 403 response after 200": later_files}, indent=2, default=str))
#print(len(file_list))
#print(count1, count2)