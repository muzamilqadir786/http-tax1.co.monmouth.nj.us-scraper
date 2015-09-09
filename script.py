import zipfile

import os
from setuptools.command.sdist import re_finder

base_dir = "c://files/"
##for root, dirs, files in os.walk(base_dir):
##    for file1 in files:
##        print '---', file
##        fh = open(base_dir+file1, 'rb')
##        z = zipfile.ZipFile(fh)
##        for name in z.namelist():
##            outpath = "C:\\files"
##            z.extract(name, outpath)
    
import re
for root, dirs, files in os.walk(base_dir):
    csv_files = [fi for fi in files if fi.endswith(".csv") ]

csv_files = filter(None,[el if re.match('^\d{4}',el) else None for el in csv_files])
print csv_files
print len(csv_files)

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

import csv
total_rows = 0
est_csv = open(base_dir+'Real_estatesdata1234567890.csv','wb')
fobj = csv.writer(est_csv,delimiter=',')
flag = False
for csv_file in csv_files:
    print csv_file
    with open(base_dir+csv_file) as f:
        rows = csv.reader(f)
        
        for ctr,row in enumerate(rows,start=1):
            if any('ESTATE' in a for a in row):
                fobj.writerow(row)
                print ctr
                continue
            for x in row:
                word = findWholeWord('EST')(x)
                if word:
                    flag = True
            if flag:
                fobj.writerow(row)
            flag = False
                
est_csv.close()

print total_rows

             
