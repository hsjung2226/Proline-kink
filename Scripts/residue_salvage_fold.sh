#!/bin/bash


out_pattern=( LPNVRYLALGGNKLHDISALKE LTNLTYLTLEPNQLQSLPNGVFDK LTNLKELQLWANQLQSLPDGVFDK LTNLTYLNLAFNQLQSLPKGVFDK LTNLTELDLSYNQLQSLPKGVFDK LTQLKDLRLYQNQLKSVPDGVFDR LTSLQYIWLHDNPWDCTCPGIRYL)


rotate_num=( 21 45 69 93 117 141 165 189 )

iter_loop=3
first_seq=${out_pattern[1]}
echo ${first_seq}
second_seq=${out_pattern[2]}

iter_residue=19
for i in {20..24}
do
		pdbxyz 4j4l_round${iter_loop}_${iter_residue}.pdb -k constant.key
		xyzpdb 4j4l_round${iter_loop}_${iter_residue}.xyz -k constant.key
		python3 coord_maker.py AF2_constant.pdb ${first_seq} ${second_seq} ${iter_loop} ${iter_residue}
		if [ $i -eq 22]
		then	
			minimize 4j4l_round${iter_loop}_${iter_residue}.xyz -k constant.key 1.0
		else
			minimize 4j4l_round${iter_loop}_${iter_residue}.xyz -k 4j4l_round${iter_loop}_${iter_residue}.key 0.5
		fi

		if [ $i -ne 24 ]
		then

			xyzpdb 4j4l_round${iter_loop}_${iter_residue}.xyz_2 -k constant.key
			mv 4j4l_round${iter_loop}_${iter_residue}.pdb_3 4j4l_round${iter_loop}_${iter_residue}_0.pdb
			pymol 4j4l_round${iter_loop}_${iter_residue}_0.pdb -cq remove_hydro_residue.py -- ${iter_loop} ${iter_residue}
			pymol 4j4l_round${iter_loop}_${iter_residue}_1.pdb -cq rotate_superimpose_residue.py -- ${iter_loop} ${iter_residue} ${rotate_num[$(expr ${iter_loop} - 2)]}

			iter_residue=`expr ${iter_residue} + 1`
		fi


done

xyzpdb 4j4l_round${iter_loop}_${iter_residue}.xyz_2 -k constant.key
mv 4j4l_round${iter_loop}_${iter_residue}.pdb_3 4j4l_round${iter_loop}_${iter_residue}_0.pdb
pymol 4j4l_round${iter_loop}_${iter_residue}_0.pdb -cq remove_hydro_residue.py -- ${iter_loop} ${iter_residue}	
pymol 4j4l_round${iter_loop}_${iter_residue}_1.pdb -cq rotate_superimpose_residue.py -- ${iter_loop} ${iter_residue} ${rotate_num[$(expr ${iter_loop} - 2)]}

cp 4j4l_round${iter_loop}_24.pdb ../modeller/4j4l_round${iter_loop}.pdb
cd ../modeller


