import glob
import json
import os

foldername = input('Enter Supervisely folder name ')

for filename in glob.glob(foldername + '/supervisely_p*_v*.json'):
    pathname, _ = os.path.splitext(filename)

    print('Begin processing file ' + filename + '\n')

    fi = open(filename)
    fo = open(pathname + '.txt', 'w')

    data = json.load(fi)

    objectids = []
    lines = []

    for o in data['objects']:
        objectids.append(o['id'])

    for f in data['frames']:
        for figure in f['figures']:
            figure['frame'] = f['index']
            figure['objectId'] = objectids.index(figure['objectId'])
            lines.append(figure)

    lines.sort(key=lambda l:(l['frame'],l['objectId']))

    for l in lines:
        e = l['geometry']['points']['exterior']
        x = max(0, min(e[0][0], e[1][0]))
        y = max(0, min(e[0][1], e[1][1]))
        line = f"{l['frame'] + 1},{l['objectId'] + 1},{x},{y},{abs(e[1][0] - e[0][0])},{abs(e[1][1] - e[0][1])},1,-1,-1,-1"
        
        print(line)
        fo.write(line + '\n')

    fi.close()
    fo.close()

    print('End processing file ' + filename + '\n')
