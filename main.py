import os
import zlib

def crc32(fileName):
    with open(fileName, 'rb') as fh:
        hash = 0
        while True:
            s = fh.read(65536)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)

# 7z l dumps prioritized as last more important
# these are obtained via `7z l -slt <7z_fname> > <7z_fname>.txt`
_7Z_DUMP_FILES = ['2023-08-16_Baldurs Gate 3.7z.txt', '2023-08-17_Baldurs Gate 3-Patch0Hotfix4.7z.txt']

# gather 7Z data
final_data = {} # contains final crc / size data per path, last file in list is prioritized
data_by_fname = {} # contains crc / size data for each file per path
for fname in _7Z_DUMP_FILES:
    with open(fname, 'r') as f:
        lines = f.readlines()

    # example block (blocks separated by empty newlines):
    # Path = Baldurs Gate 3\bin\gold.2023-08-10T17-29-33-191773.log
    # Size = 17317
    # Packed Size = 
    # Modified = 2023-08-10 17:52:34.0768743
    # Attributes = A
    # CRC = 12F9B287
    # Encrypted = -
    # Method = LZMA2:25
    # Block = 0
    
    cur_path = ''
    cur_size = '0'
    cur_crc = ''
    data = {}
    for line in lines:
        # flush on empty lines
        if line.strip() == '':
            if cur_path != '' and cur_size != '0' and cur_crc != '':
                data[cur_path] = {'size': int(cur_size), 'crc': cur_crc}
            cur_path = ''
            cur_size = '0'
            cur_crc = ''
        elif line.startswith('Path = '):
            cur_path = line.strip()[7:]
        elif line.startswith('Size = '):
            cur_size = line.strip()[7:]
        elif line.startswith('CRC = '):
            cur_crc = line.strip()[6:]
            print(f'"{cur_path}" "{cur_size}" "{cur_crc}"')
            # CRC is usually last attribute we care about, so should be safe to assign here
            if cur_path != '' and cur_size != '0' and cur_crc != '':
                data[cur_path] = {'size': int(cur_size), 'crc': cur_crc}
    data_by_fname[fname] = data
    
    for path in data:
        final_data[path] = data[path]
        final_data[path]['last_src_fname'] = fname

DIR_TO_DIFF = "Baldur's Gate 3"
# gather actual directory info
new = []
diff_size = []
diff_crc = []
for root, dirs, files in os.walk(DIR_TO_DIFF):
    # print(root, dirs, files)
    for file in files:
        path = os.path.join(root, file)
        print('working', path)
        if path not in data:
            print(path, 'is new')
            new.append(path)
            continue
        size = os.path.getsize(path)
        if data[path]['size'] != size:
            print(path, 'has diff size, must be different')
            diff_size.append(path)
            continue
        crc = crc32(path)
        if data[path]['crc'] != crc:
            print(path, 'has diff crc, must be different')
            diff_crc.append(path)
            continue
        print(path, 'is unchanged')

print('---new---')
for _ in new: print(_)
print('---diff_size---')
for _ in diff_size: print(_)
print('---diff_crc---')
for _ in diff_crc: print(_)
