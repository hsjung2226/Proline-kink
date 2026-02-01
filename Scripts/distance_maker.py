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

FN = sys.argv[1]

data = open(FN, "r").readlines()
pair = seq_generator(data)

seq = [a for (a,b) in pair]
position_num = [b for (a,b) in pair]


#pair selection upon last loop

last_seq_in = sys.argv[2]

last_pair = []
pattern = re.compile(last_seq_in)
result = pattern.search("".join(seq))

start = result.span()[0]
end = result.span()[-1]
arr_index = range(start, end) 

for num in arr_index :
    last_pair.append(position_num[num])

#pair selection upon new loop

new_seq_in = sys.argv[3]

new_pair = []
pattern = re.compile(new_seq_in)
result = pattern.search("".join(seq))

start = result.span()[0]
end = result.span()[-1]
arr_index = range(start, end) 

for num in arr_index :
    new_pair.append(position_num[num])

    
# upload position key file
iter_num = sys.argv[4]
iter_num = int(iter_num)

position_data = open("position_%s.key"%(iter_num)).readlines()

# making new key file
iter_pair_num = sys.argv[5]
iter_pair_num = int(iter_pair_num)

new_key = open("4j4l_round%s_%s.key"%(iter_num, iter_pair_num), "w")
# all pair has different boundaries
range_dic = {'0' : (6.589627265930176, 6.949747085571289),
             '1' : (6.637403964996338, 7.0505218505859375),
             '2' : (6.052547454833984, 6.353446960449219),
             '3' : (5.6185712814331055, 5.85136604309082),
             '4' : (5.1142354011535645, 5.323873043060303),
             '5' : (4.729222297668457, 4.853963375091553),
             '6' : (4.960053443908691, 5.073302745819092),
             '7' : (4.569969177246094, 4.811351299285889),
             '8' : (5.056571960449219, 5.405867576599121),
             '9' : (4.7952046394348145, 6.465261459350586),
             '10' : (4.713855266571045, 7.479618072509766),
             '11' : (4.155730247497559, 6.26751708984375),
             '12' : (5.43218469619751, 7.59856653213501),
             '13' : (5.726025581359863, 8.607699394226074),
             '14' : (6.0692667961120605, 7.699207305908203),
             '15' : (6.3224005699157715, 8.499645233154297),
             '16' : (5.843703746795654, 8.252765655517578),
             '17' : (7.26919412612915, 9.80502700805664),
             '18' : (7.886357307434082, 10.485424995422363),
             '19' : (7.610555171966553, 8.23305606842041),
             '20' : (6.944591999053955, 7.754744052886963),
             '21' : (6.910841941833496, 7.094748020172119),
             '22' : (7.56371545791626, 7.8505706787109375),
             '23' : (7.337845325469971, 7.600836277008057) 
             }

#writing dowm position restrain
if iter_pair_num == 0 :
    for line in position_data :
        new_key.write(line)
        
else : 
    key_data = open("4j4l_round%s_%s.key"%(iter_num, iter_pair_num -1)).readlines()
    for line in key_data :
        new_key.write(line)
        

#writing_down distance restrain
pos_pos =  list(zip(last_pair, new_pair))
print(last_pair)
print(new_pair)



#pos_pos = pos_pos[::-1]




try :
    new_key.write("restrain_distance {} {} 10000.0 {:.2f} {:.2f}".format(pos_pos[iter_pair_num][0], pos_pos[iter_pair_num][1], range_dic[str(iter_pair_num)][0], range_dic[str(iter_pair_num)][1] + 0.01))
    print(pos_pos[iter_pair_num][0], pos_pos[iter_pair_num][1])
    new_key.write("\n")
except IndexError :
    if iter_pair_num == 22 :
        new_key.write("restrain-distance {} {} 1000.0 7.28 7.34").format(last_pair[-2], new_pair[-2])
        new_key.write("\n")
    elif iter_pair_num == 23 :
        new_key.write("restrain-distance {} {} 1000.0 6.36 6.42").format(last_pair[-1], new_pair[-1])
        new_key.write("\n")
new_key.close()
