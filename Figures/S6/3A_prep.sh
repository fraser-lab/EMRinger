cd 3A
for i in 84 131 300 422 651 857 1381 1438 1444 1607; do
	 cd $i
	 echo $i
	 for j in *.pdb; do
	 	echo $j 
	 	phenix.python ../../../../Phenix_scripts/emringer.py $j ../../emd_5778.map output_base=$j >> ringer.log
	 	phenix.python ../../../../Phenix_scripts/emringer_analysis.py -i $j.pkl >> scores.txt
	 done
	 cd ../
done
cd ../