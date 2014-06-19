#!/usr/bin/python

import sys, os

for i in range(1, 23):
 	cmd = "echo 'python interpolate_maps.py ~/1kG_data/imputation_reference/annot_noextend/chr"+str(i)+".bed.gz ~/Databases/human_genome/hg19/genetic_map/1kG_OMNI/CEU/CEU-"+str(i)+"-final.txt.gz  chr"+str(i)+".OMNI.interpolated_genetic_map.gz' | qsub -q res.q -cwd -o /dev/null -e /dev/null -V"
	print cmd
	os.system(cmd)
