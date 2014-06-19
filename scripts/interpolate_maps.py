#!/usr/bin/python


import sys, os, gzip

infile = gzip.open(sys.argv[1]) #.bed
mapfile = gzip.open(sys.argv[2]) #input map file, either the HapMap map or the 1000 Genomes OMNI map
outfile = gzip.open(sys.argv[3], "w") #output style: [rs] [pos] [genetic pos]

posin = list()
rsin = list()
mappos = list()
mapgpos = list()

line = infile.readline()
while line:
	line = line.strip().split()
	pos = int(line[2])
	rs = line[3]
	posin.append(pos)
	rsin.append(rs)
	line = infile.readline()

line = mapfile.readline()
line = mapfile.readline()
while line:
	line = line.strip().split()
	pos = int(line[0])
	#pos = int(line[1]) #uncomment for hapmap input
	gpos = float(line[2])
	#gpos = float(line[3]) #uncomment for hapmap  input
	mappos.append(pos)
	mapgpos.append(gpos)
	line = mapfile.readline()

index1 = 0
index2 = 0
while index1 < len(posin):
	pos = posin[index1]
	rs = rsin[index1]
	if pos == mappos[index2]:
		#the 1000 Genomes site was genotyped as part of the map
		print >> outfile, rs, pos, mapgpos[index2]
		print rs, pos, mapgpos[index2]
		index1 = index1+1
	elif pos < mappos[index2]:
		#current position in interpolation before marker
		if index2 ==0:
			#before the first site in the map (genetic position = 0)
			print >> outfile, rs, pos, mapgpos[index2]
			index1 = index1+1
		else:
			#interpolate
			prevg = mapgpos[index2-1]
			prevpos = mappos[index2]
			frac = (float(pos)-float(mappos[index2-1]))/ (float(mappos[index2]) - float(mappos[index2-1]))
			tmpg = prevg + frac* (mapgpos[index2]-prevg)
			print >> outfile, rs, pos, tmpg
			print rs, pos, tmpg
			index1 = index1+1
	elif pos > mappos[index2]:
		#current position in interpolation after marker
		if index2 == len(mappos)-1:
			#after the last site in the map (genetic position = maximum in map, note could try to extrapolate based on rate instead)
			print >> outfile, rs, pos, mapgpos[index2]
			print rs, pos, mapgpos[index2]
			index1 = index1+1
		else:
			#increment the marker
			index2 = index2+1
