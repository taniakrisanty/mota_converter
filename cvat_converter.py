import glob
import os
import pandas
from zipfile import ZipFile

foldername = input('Enter CVAT folder name ')

for filename in glob.glob(foldername + '/cvat_p*_v*.zip'):
    pathname, _ = os.path.splitext(filename)

    print('Begin processing file ' + filename + '\n')

    with ZipFile(filename) as zip:
        zip.extract('gt/gt.txt', path=pathname)
        
        data = pandas.read_csv(pathname + '/gt/gt.txt')
        data[''] = '-1'
        for i in range(len(data.index)):
            data.iat[i, 6] = '1'
            data.iat[i, 7] = '-1'
            data.iat[i, 8] = '-1'
            
        data.to_csv(pathname + '.txt', header=False, index=False)
    zip.close()

    print('End processing file ' + filename + '\n')
