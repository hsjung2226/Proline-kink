#!/bin/bash

cd ../modeller


out_pattern=( LPNVRYLALGGNKLHDISALKE LTNLTYLTLEPNQLQSLPNGVFDK LTNLKELQLWANQLQSLPDGVFDK LTNLTYLNLAFNQLQSLPKGVFDK LTNLTELDLSYNQLQSLPKGVFDK LTQLKDLRLYQNQLKSVPDGVFDR LTSLQYIWLHDNPWDCTCPGIRYL)

iter_loop_num=`find ../modeller  -name '*.ali' | wc -l`

rotate_num=( 21 45 69 93 117 141 165 189 )

for iter_loop in `seq 4 ${iter_loop_num}`
do
	if [ "${iter_loop}" -eq 1  ]
	then 
		#python3 modeller_maker.py 4j4l_round1.ali 4j4l_round1 4j4l
		echo "____________________________________________________________________________________________________________________________"
		continue
	
	elif [ "${iter_loop}" -ne 1 ]
	then
		python3 modeller_maker.py 4j4l_round${iter_loop}.ali 4j4l_round${iter_loop} 4j4l_round$(expr ${iter_loop} - 1)
	fi

	
	pdbxyz 4j4l_round${iter_loop}.pdb -k ../tinker4/constant.key 
	minimize 4j4l_round${iter_loop}.xyz -k ../tinker4/constant.key 1.0
	xyzpdb 4j4l_round${iter_loop}.xyz_2 -k ../tinker4/constant.key


	cp 4j4l_round${iter_loop}.pdb_2 ../tinker4/4j4l_round${iter_loop}_0_1.pdb
	cp 4j4l_round$(expr ${iter_loop} - 1).pdb  ../tinker4/4j4l_round$(expr ${iter_loop} - 1).pdb
	cd ../tinker4

	pymol 4j4l_round${iter_loop}_0_1.pdb -cq remove_hydro.py -- ${iter_loop}
	pymol 4j4l_round${iter_loop}_0_2.pdb -cq superimpose.py -- ${iter_loop} ${rotate_num[$(expr ${iter_loop} - 2)]} "4j4l_round${iter_loop}_0_2"
		
	out_seq=''
	for ele in ${out_pattern[@]}
	do
		out_seq+="${ele}"
		

		if [ "${ele}" == "${out_pattern[$(expr ${iter_loop} - 1)]}" ]
		then
			
			break
		fi
	done
	echo "out_seq : ${out_seq}"

	first_seq=${out_pattern[$(expr ${iter_loop} - 2)]}
	second_seq=${out_pattern[$(expr ${iter_loop} - 1)]}
	
	echo "first_seq : ${first_seq}"
	echo "second_seq : ${second_seq}"

	iter_residue=0
	for i in {1..24}
	do
			pdbxyz 4j4l_round${iter_loop}_${iter_residue}.pdb -k constant.key
			xyzpdb 4j4l_round${iter_loop}_${iter_residue}.xyz -k constant.key
			python3 coord_maker.py AF2_constant.pdb ${first_seq} ${second_seq} ${iter_loop} ${iter_residue}
			if [ $i -eq 22]
			then	
				minimize 4j4l_round${iter_loop}_${iter_residue}.xyz -k constant.key 1.0
			else
				minimize 4j4l_round${iter_loop}_${iter_residue}.xyz -k 4j4l_round${iter_loop}_${iter_residue}.key 1.0
			fi

			if [ $i -ne 24 ]
			then

				xyzpdb 4j4l_round${iter_loop}_${iter_residue}.xyz_2 -k constant.key
				mv 4j4l_round${iter_loop}_${iter_residue}.pdb_3 4j4l_round${iter_loop}_${iter_residue}_0.pdb
				pymol 4j4l_round${iter_loop}_${iter_residue}_0.pdb -cq remove_hydro_residue.py -- ${iter_loop} ${iter_residue}
				mv 4j4l_round${iter_loop}_${iter_residue}_1.pdb 4j4l_round${iter_loop}_$(expr ${iter_residue} + 1 ).pdb
				iter_residue=`expr ${iter_residue} + 1`
		 	fi
	

	done
	
	xyzpdb 4j4l_round${iter_loop}_${iter_residue}.xyz_2 -k constant.key
	mv 4j4l_round${iter_loop}_${iter_residue}.pdb_3 4j4l_round${iter_loop}_${iter_residue}_0.pdb
	pymol 4j4l_round${iter_loop}_${iter_residue}_0.pdb -cq remove_hydro_residue.py -- ${iter_loop} ${iter_residue}	
	pymol 4j4l_round${iter_loop}_${iter_residue}_1.pdb -cq rotate_superimpose_residue.py -- ${iter_loop} ${iter_residue} ${rotate_num[$(expr ${iter_loop} - 2)]}

	cp 4j4l_round${iter_loop}_24.pdb ../modeller/4j4l_round${iter_loop}.pdb
	cd ../modeller
done
 
