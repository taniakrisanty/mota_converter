import glob
import json
import numpy
import os

foldername = input('Enter Label Studio folder name ')

for filename in glob.glob(foldername + '/labelstudio_p*.json'):
    pathname, _ = os.path.splitext(filename)

    print('Begin processing file ' + filename + '\n')

    fi = open(filename)

    data = json.load(fi)

    for d in data:
        lines = []

        videoname, _ = os.path.splitext(d['file_upload'])
        videoname = videoname.split('-', 1)[1]

        fo = open(pathname + '_' + videoname + '.txt', 'w')

        for a in d['annotations']:
            i = 1
            for r in a['result']:
                for s in r['value']['sequence']:
                    s['id'] = i
                    lines.append(s)
                i += 1

        lines.sort(key=lambda l:l['frame'])

        original_w = original_h = 1
        match videoname:
            case 'v1':
                original_w = 612
                original_h = 184
            case 'v2':
                original_w = 1280
                original_h = 720
            case 'v3' | 'v4':
                original_w = 640
                original_h = 480

        for l in lines:
            x = max(0, l['x'] / 100.0 * original_w)
            y = max(0, l['y'] / 100.0 * original_h)
            w = l['width'] / 100.0 * original_w
            h = l['height'] / 100.0 * original_h
            line = f"{l['frame']},{l['id']},{numpy.format_float_positional(x, trim='-')},{numpy.format_float_positional(y, trim='-')},{w},{h},1,-1,-1,-1"
        
            print(line)
            fo.write(line + '\n')

        fo.close()

    fi.close()

    print('End processing file ' + filename + '\n')
