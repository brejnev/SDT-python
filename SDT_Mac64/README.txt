SDT_Mac64 (Sequence Demarcation Tool - Mac OSX 64 bits)
======================================================

SDT_Mac64 is a free version of SDT written in python, which runs on Mac OSX 64 bits operating system.
 
Given a FASTA file containing DNA sequences, the program aligns all possible pairs of sequences using Muscle (Edgar, 2004), 
ClustalW2 (Larkin et al., 2007)  or Mafft (Katoh et al., 2009), calculates the sequence similarity score for each pair and 
uses a rooted neighbour joining phylogenetic tree to cluster closely related sequences based on similarity scores.
It outputs the results into a ".sdt" file that can be open with SDTv.1.0 Windows version to visualise the plot and similarity matrix
images and save the output in various formats. It also writes scores into a text file.
The similarity scores are calculated as 1-(M/N) where M is the number of mismatching nucleotides and N is the total number of positions along the alignment where neither sequence has a gap character. 

DOWNLOAD AND INSTALLATION
==============================
1. Software requirements:

   The program requires the following to be installed:

   - Python2.7 

2. Dowload the SDT_Mac64 from http://web.cbio.uct.ac.za/SDT

3. Extract the SDT_Mac64.tar file into the location you want to place the program.
   The folder contains:
      - The bin directory which contains the executable files "muscle3.8.31_i86darwin64", "clustalw2" and "neighbor".     
      - The Bio directory which contains the Biopython library.
      - The output directory in which the output files after each run are stored.
      - SDT_Mac64.py which the main script of the program.
      - test.fas a sample FASTA file to test the program.

4. Please change the mode of "muscle3.8.31_i86darwin32", "clustalw2" and "neighbor" in the bin directory to "executable". 

5. Running commands:
	
	python SDT_Mac64.py test.fas muscle

	This will result in the use of MUSCLE as the alignment program. Replace "muscle" by "clustal" or "mafft" (if mafft is installed) 
	to change the alignment program that is used. When the pairwise alignments and similarity score calculations are completed the scores will be written 
	into a text file named after the input FASTA file and save into the output folder and a ".sdt" file will be produced which can be open by the 
	SDTv.1.0 windows version to easily produce the plot, matrix and data. 

-------------------------------------------------------------------------------------------------------------------------------------------------------

References 
----------
1. Edgar, Robert C. (2004), MUSCLE: multiple sequence alignment with high accuracy and high
throughput, Nucleic Acids Research 32, 1792-1797. 
 
2. Larkin MA, Blackshields G, Brown NP, Chenna R, McGettigan PA, McWilliam H, Valentin F,
Wallace IM, Wilm A, Lopez R, Thompson JD, Gibson TJ, Higgins DG. 
(2007). Clustal W and Clustal X version 2.0., Bioinformatics 23, 2947-2948 
 
3. Katoh K, Asimenos G, Toh H. (2009) Multiple Alignment of DNA Sequences with MAFFT,
Methods in Molecular Biology 537:39-64  
 
4. Felsenstein, J. (1995)PHYLIP (Phylogeny Inference Package) Version 3.57c, available at
http://www.med.nyu.edu/rcr/rcr/phylip/main.html#refs 

Authors  
-------

Brejnev Muhire [1]
Darren Martin [1]
Arvind Varsani [2]

[1] Institute of Infectious Diseases and Molecular Medicine (IIDMM)
    Computational Biology Group, 
    University of Cape Town
    South Africa 
[2] School of Biological Sciences 
    University of Canterbury
    Private Bag 4800 
    Christchurch, 8140
    New Zealand
BM is funded by the University of Cape Town
website: http://web.cbio.uct.ac.za/SDT                
email: mhrbre001@myuct.ac.za
email: mubrejnev@gmail.com	
