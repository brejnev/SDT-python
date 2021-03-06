#############################################                                
# Sequence Demarcation Tool (Mac OSX 32 bits)#
#         Written by Brejnev Muhire         #
#          University of Cape Town          #
#	      	    Feb 2014                #
#############################################

import os, sys, time, shutil,subprocess
from subprocess import *
from Bio import SeqIO

#********************************** getting the running parameters ******************************
if len(sys.argv)<=2: 
	print "Please specify the input fasta file and the alignment program properly e.g.: python SDT_Mac32.py test.fas muscle"
	sys.exit(0)
else:
	INPUT_PATH=sys.argv[1]
	fname=INPUT_PATH.split("/")[-1]
	if os.path.exists(INPUT_PATH)==False:
		print "The input file %s cannot be found, please make sure the file is in the program directory"%fname
		sys.exit(0)
	alg=sys.argv[2]
	if alg!="muscle" and alg!="clustalw" and alg!="mafft":
		print "Please specify the alignment program correctly e.g. muscle or clustalw or mafft"
		sys.exit(0)	

#****** path to alignment programs : these can be changed to locations where you have installed the programs on your system******

MUSCLE_PATH=os.getcwd()+"/bin/muscle3.8.31_i86darwin32" 				# the path to muscle

CLUSTALW_PATH=os.getcwd()+"/bin/clustalw2" 					# the path to clustalW2

MAFFT_PATH="/xxx/mafft" 						        # the path to mafft: if you want to use mafft for alignment, please install it on your system and change this path to the location where mafft executable is located.

NEIGHBOR_PATH=os.getcwd()+"/bin/neighbor"					# the path to neighbor

#****************************************************working directories ************************************
WRK_DIR=os.getcwd()								# location of this script (SDTMPI.py)

BIN_DIR=os.getcwd()+"/bin/"							# the output directory

OUT_DIR=os.getcwd()+"/output/" 							# the output directory

#****************************************************** functions ********************************************

# This function aligns sequences using muscle and wait for muscle to finish 
def Align_Wait(IN,OUT,algorithm):
	if algorithm=="muscle":
		cmd=[MUSCLE_PATH,'-in', IN,'-out',OUT] # muscle's path, input name and out put name

	elif algorithm=="clustalw":
		cmd=[CLUSTALW_PATH,'-INFILE='+IN,'-OUTFILE='+OUT,"-type=DNA"]

	elif algorithm=="mafft":
		cmd=[MAFFT_PATH,'--quiet','--localpair',IN]	
	
	proc=Popen(cmd,stdout=PIPE,stderr=PIPE)
	(output, error)=proc.communicate()
	return_code = proc.wait()

	if return_code != 0:
    		sys.stderr.write(error)
    		sys.exit(1)

	if algorithm=="mafft":
		h=open(OUT,"w")
		h.write(output)
		h.close()
	
# THis function that takes a fasta file containing two sequences and calculate the similarity score
def Get_Similarity(InSeq,algorithm):
	dist=0
	gaps=0
	recs=[]
	hndlr=open(InSeq,"r")
	if algorithm=="muscle" or algorithm=="mafft":
		for record in SeqIO.parse(hndlr, "fasta") :
			recs.append(record)
	elif algorithm=="clustalw":
		for record in SeqIO.parse(hndlr, "clustal") :
			recs.append(record)
	for i in range(len(recs[0].seq)):
		if recs[0].seq[i]!="-" and recs[1].seq[i]!="-":
			if recs[0].seq[i]!=recs[1].seq[i]:
				dist+=1
		else:
			gaps+=1
	similarity=1-(float(dist)/(len(recs[0].seq)-gaps))
	#print "Sim ",similarity, " gaps ", gaps,"dis ", dist 
	return similarity



#************************************************************ main code *********************************************************************************

#timing
starting=time.time()
print "Loading sequences"

#read the records	       
In_Handle = open(INPUT_PATH, "r")
List_Rec=[]

NumSeqs=0
for record in SeqIO.parse(In_Handle, "fasta") :
	List_Rec.append(record)
	NumSeqs+=1
In_Handle.close()

#Calculation of the number of pairs to be aligned
TotPairs= float(len(List_Rec)*len(List_Rec)-len(List_Rec))/2


# creating lists that gives the paiwise combination of the indexes of the two sequences to align. 
# for example for a fas file containing 5 sequences the list will contained: l1=[0,0,0,0,1,1,1,2,2,3], l2=[1,2,3,4,2,3,4,3,4,4] 
# they both give the following paires (0,1)(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4). 
l1=[]
l2=[]
for i in range(len(List_Rec)+1):
	for j in range(i+1,len(List_Rec)):
		l1.append(i)
		l2.append(j)


#File_out_name=OUT_DIR+str(start_in)+"_"+str(ending_in)+"_"+str(myrank)+".txt" #out put file name

h_out_col=open(OUT_DIR+fname+"_identity_scores.txt","w")
h_out_col.write('First sequence, Second sequence, Identity Score \n')
dic_id_score={}

CounterPairs=0
for i in range(len(l1)):
	name_in=BIN_DIR+str(l1[i])+"__"+str(l2[i])+".fas"          #name of alignment input file
	name_out=BIN_DIR+str(l1[i])+"__"+str(l2[i])+"algn.fas"     #name of alignment output file
	Out_Handle = open(name_in, "w")
	
	List_Rec[l1[i]].seq=List_Rec[l1[i]].seq.ungap("-") #removing gaps
	List_Rec[l2[i]].seq=List_Rec[l2[i]].seq.ungap("-") #removing gaps
		
	SeqIO.write(List_Rec[l1[i]], Out_Handle, "fasta") #writing the first sequence in the file input file
	SeqIO.write(List_Rec[l2[i]], Out_Handle, "fasta") #writing the second sequence in the file input file
	Out_Handle.close()

	CounterPairs=	CounterPairs+1
	sys.stdout.write("\rPerforming pairwise alignment: progress " + str(int((float(CounterPairs)/TotPairs)*100))+"%")
	sys.stdout.flush()
		
	Align_Wait(name_in,name_out,alg)                      #calling muscle 
	os.remove(name_in)	#removing the alignment input file

	if alg=="clustalw":
		dnd=BIN_DIR+str(l1[i])+"__"+str(l2[i])+".dnd"
		os.remove(dnd)	

	dic_id_score[str(l1[i]) + "_" + str(l2[i])]=Get_Similarity(name_out,alg)
	dic_id_score[str(l2[i]) + "_" + str(l1[i])]=Get_Similarity(name_out,alg)

	h_out_col.write( List_Rec[l1[i]].id + "," + List_Rec[l2[i]].id+ "," + str(Get_Similarity(name_out,alg)) +"\n") # writing the indexes and names of the two aligned sequences and the corresponding similarity score
	os.remove(name_out) # removing the alignment output file



os.chdir(BIN_DIR)                 # change to the bin directory

#**************** create the distance matrix, and runNeigbor.sh file ********************************

print "\rCreating the distance matrix"

#kill existing tmp file
if os.path.exists("infile"):
	os.remove("infile")
if os.path.exists("outfile"):
	os.remove("outfile")
if os.path.exists("outtree"):
	os.remove("outtree")
	
h_out=open("infile","w")

h_out.write("   "+str(NumSeqs+1)+"\n")
	
for i in range(NumSeqs+1):
	if i<NumSeqs:
		name1=List_Rec[i].id.replace(" ","_")
		name1=name1.replace(":","_")
		name1=name1.replace("-","_")
		name1=name1.replace("(","_")
		name1=name1.replace(")","_")
		name=str(i)+"_"+name1

		if len(name)<=10:
			name=name+" "*(12-len(name))
		elif len(name)>10:
			name=name[0:10]+"  "			
		h_out.write(name+"\t")
		for j in range(NumSeqs+1):
			if j<(NumSeqs):			
				if i==j:
					h_out.write("0.0000  ")
				if i<j:
					key_=str(i)+ "_"+ str(j)
					score=str(round(1-dic_id_score[key_],4))
					if len(score)<6:
						score=score+"0"*(6-len(score))
					h_out.write(score+"  ")
				if i>j:
					key_=str(j)+"_"+str(i)
					score=str(round(1-dic_id_score[key_],4))
					if len(score)<6:
						score=score+"0"*(6-len(score))				
					h_out.write(score+"  ")
			elif j==NumSeqs:
				h_out.write("1\n")
	elif i==NumSeqs:
		h_out.write("out       "+"\t")
		for j in range(NumSeqs+1):
			if j<NumSeqs:
				h_out.write(str(1)+"  ")
			elif j==NumSeqs:
				h_out.write("0\n")
				
h_out.close()

#******************************** run neighbor *************************************
print "Drawing the phylogenetic tree..."

#shell file	
h_sh=open("runNeighbor.sh","w")		
h_sh.write("#!/bin/bash\n")
h_sh.write(NEIGHBOR_PATH+" <<EOD\n")
h_sh.write("infile\n")
h_sh.write("O\n")
h_sh.write(str(NumSeqs+1)+"\n")
h_sh.write("Y\n")
h_sh.write("EOD\n")
h_sh.close()
	
#run neighbor
cmd=["chmod", "+x", "runNeighbor.sh"]
proc=Popen(cmd,stdout=PIPE,stderr=PIPE)
(output, error)=proc.communicate()
return_code = proc.wait()
if return_code != 0:
    	sys.stderr.write(error)
    	#sys.exit(1)

cmd="./runNeighbor.sh"
proc=Popen(cmd,stdout=PIPE,stderr=PIPE)
(output, error)=proc.communicate()
return_code = proc.wait()
if return_code != 0:
    	sys.stderr.write(error)
    	#sys.exit(1)
os.remove("infile")	
os.remove("outfile")
os.remove("runNeighbor.sh")

#****************************** create mapping ************************************
	
h_out=open("outtree","r").read()
l=h_out.split(",")
MappingArr=[]
for x in range(NumSeqs+1):
	l[x]=l[x].replace(")","")
	l[x]=l[x].replace("(","")
	l[x]=l[x].replace(" ","")
	l[x]=l[x].replace("\t","")
	l[x]=l[x].replace("\n","")
	CurrName=l[x].split(":")[0]
	CurrName=CurrName.split("_")[0]
	MappingArr.append(CurrName)
os.remove("outtree")
	
os.chdir(WRK_DIR)
	
#******* writing pairwise identity score matrix and the output SDT file ***********

print "\rWriting pairwise identity scores..."

h_out_sdt=open(OUT_DIR+fname+".sdt","w")


for i in range(NumSeqs):
	if i==0 :
		h_out_sdt.write("[[[>"+List_Rec[int(MappingArr[i])].id+"\r\n")
		h_out_sdt.write(str(List_Rec[int(MappingArr[i])].seq)+"\r\n")
	elif i==NumSeqs-1:
		h_out_sdt.write(">"+List_Rec[int(MappingArr[i])].id+"\r\n")
		h_out_sdt.write((str(List_Rec[int(MappingArr[i])].seq)).rstrip("\r\n")+"]]]\r\n")
	else:
		h_out_sdt.write(">"+List_Rec[int(MappingArr[i])].id+"\r\n")
		h_out_sdt.write(str(List_Rec[int(MappingArr[i])].seq)+"\r\n")
	


h_out_mat=open(OUT_DIR+fname+"_mat.txt","w")


for i in range(NumSeqs):
	mat_raw=List_Rec[int(MappingArr[i])].id
	for j in range(NumSeqs):
		if i<j:
			#mat_raw=mat_raw+",NaN"
			continue
		elif i==j:
			mat_raw=mat_raw+",1.000"
			
		elif i>j:
			key_1=str(MappingArr[i])+"_"+str(MappingArr[j])
			h_out_sdt.write(str(dic_id_score[key_1])+"\r\n")				
			mat_raw=mat_raw+","+str(dic_id_score[key_1])


	h_out_mat.write(mat_raw+"\n")


h_out_sdt.close()
h_out_mat.close()

ending=time.time()

print "\rRunning cmd: python SDT_Mac.py %s %s\nNumber of sequences: %d \nNumber of total pairs aligned %d \n------------------------- successfuly completed -----------------------"%(INPUT_PATH,alg,len(List_Rec),TotPairs)
print "duration: "+ str((ending-starting)/60) + " min / "  + str(ending-starting) + " sec\n****************************** End ******************************"
	





