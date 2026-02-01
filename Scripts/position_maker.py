import re
import sys

def seq_generator(data) :
    box = []
    position_num = []
    for line in data :
        arr = [ele for ele in line.split(' ') if ele != '']
        if not line.startswith('ATOM') :
            continue
        if arr[2] == 'CA' :
            box.append(arr[3])
            position_num.append(arr[1])
    aa_dic = {'PRO' : 'P',
              'ILE' : 'I',
              'LYS' : 'K',
              'GLN' : 'Q',
              'PHE' : 'F',
              'ALA' : 'A',
              'GLU' : 'E',
              'ASN' : 'N',
              'LEU' : 'L',
              'SER' : 'S',
              'VAL' : 'V',
              'ASP' : 'D',
              'GLY' : 'G',
              'TYR' : 'Y',
              'ARG' : 'R',
              'HIS' : 'H',
              'CYS' : 'C',
              'THR' : 'T',
              'TRP' : 'W',
              'MET' : 'M',
              'CYX' : 'C'}

    converted = []
    for info in box :
        converted.append(aa_dic[info])

    seq = "".join(converted)
    pair = list(zip(seq, position_num)) 
    return pair

#uploading fils as milestone
FN = sys.argv[1]

data = open(FN, "r").readlines()
pair = seq_generator(data)

seq = [a for (a,b) in pair]
position_num = [b for (a,b) in pair]

#print("".join(seq))
#pair selection upon last loop

last_seq_in = sys.argv[2]

last_pair = []
pattern = re.compile(last_seq_in)
result = pattern.search("".join(seq))
print(result)
start = result.span()[0]
end = result.span()[-1]
arr_index = range(start, end ) 

for num in arr_index :
    last_pair.append(position_num[num])

#uploading new file
iter_num = sys.argv[3]
temp_position = open("position_%s.key"%(iter_num), "w")

#writing down new position restrain
temp_position.write("parameters /home/2226jhs/bin-linux/params/amber99.prm\nforcefield /home/2226jhs/bin-linux/params/amber99.prm\nCUDA-DEVICE 0\nverbose\n")

for line in data :
    out_line = [ele.replace("\n", "") for ele in line.split(' ') if ele != '']
    if not out_line[0].startswith('ATOM') :
        continue
    if out_line[1] in last_pair   :
        temp_position.write("restrain-position %s %s %s %s 1.0"%(out_line[1], out_line[-3], out_line[-2], out_line[-1]))
        temp_position.write("\n")

temp_position.close()
