import glob
import os
import xmltodict

foldername = input('Enter VATIC folder name ')

for filename in glob.glob(foldername + '/vatic_p*_v*.xml'):
    pathname, _ = os.path.splitext(filename)

    print('Begin processing file ' + filename + '\n')

    fi = open(filename)
    fo = open(pathname + '.txt', 'w')

    d = xmltodict.parse(fi.read())

    lines = []

    i = 1

    for o in d['annotation']['object']:
        for p in o['polygon']:
            p['id'] = i
            lines.append(p)
        i += 1

    lines.sort(key=lambda l:int(l['t']))

    for l in lines:
        x = max(0, int(l['pt'][0]['x']))
        y = max(0, int(l['pt'][0]['y']))
        line = f"{int(l['t']) + 1},{l['id']},{x},{y},{int(l['pt'][2]['x']) - x},{int(l['pt'][2]['y']) - y},1,-1,-1,-1"

        print(line)
        fo.write(line + '\n')

    fi.close()
    fo.close()

    print('End processing file ' + filename + '\n')
