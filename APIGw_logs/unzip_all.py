# Fernando Carmona 
# 14 Aug 2019
# Script to unzip all CloudWatch logs, which come each inside a folder and zipped
# Modify path to your own needs

import os, gzip

path = '/Users/fca/Downloads/26027df5-e55d-4239-92b6-e9b7085add8b/'
count = 0
#directories = os.system('ls')
for r, d, f in os.walk(path):
    for directory in d:
        new_path = os.path.join(path, directory)
        dest_path = os.path.join('/Users/fca/Downloads/testZip/', str(count))
        #print(new_path)
        for r, d, f in os.walk(new_path):
            for zip_file in f:
                #print(zip_file)
                ext = os.path.splitext(zip_file)[-1].lower()
                if ext == '.gz':
                    zip_path = os.path.join(new_path, zip_file)
                    try:
                        with gzip.open(zip_path, 'rb') as f_in:
                            with open(dest_path, 'wb') as f_out:
                                for line in f_in:
                                    f_out.write(line)
                            #os.system('mv {} /Users/fca/Downloads/testZip/{}'.format(new_file, count))
                            #print(dir(f_in))
                    except FileNotFoundError: 
                        print("Error")
                else:
                    print(zip_file)
        count += 1