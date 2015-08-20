#Second nanopore run

	1. dowloaded sequences, both fail and pass files
	2. use poretools for stats and to convert fast5 to fastq 


###Stats
*fail*

1. poretools stats fail/ 

		total reads	15022
		total base pairs	32880662
		mean	2188.83
		median	681
		min	7
		max	163265
		N25	14160
		N50	6550
		N75	2603

*pass*

2. poretools stats pass/

		total reads	2952
		total base pairs	7257662
		mean	2458.56
		median	995
		min	167
		max	34752
		N25	10878
		N50	5003
		N75	2970

##Converting files from fast5 to fastq 

**WD: /mnt/data3/lah/nanopore**

*fail*

1. poretools fastq  --min-length 1000 fail/ > nanopore2.harmonia.fail.fastq
2. abyss-fac nanopore2.harmonia.fail.fastq
		
		n=5943	n50=8034
		
3. poretools fastq --min-length 500 fail/ > nanopore2.harmonia.fail.2.fast
4. abyss-fac nanopore2.harmonia.fail.2.fastq 

		n=8956 n50=7309
		
*abyss-fac of old data*

1. abyss-fac nanopore.harmonia.fastq	

		n=19802 N50=11205
		
		
**Go with min-length of 1000 b/c the reads between 500 and 1000 might just muck up assembler** 

*pass*

1. poretools fastq --min-length 1000 pass/ > nanopore2.harmonia.pass.fastq
2. abyss-fac nanopore2.harmonia.pass.fastq 

		n=1472 N50=6210
	
##concatenating fail/pass and old nanopore data 
1. cat nanopore2.harmonia.fail.fastq nanopore2.harmonia.pass.fastq nanopore.harmonia.fastq > nanopore.all.fastq


##nanocorrect to correct all.fastq file
**WD:/mnt/data3/lah/nanopore/nanocorrect2**

1. mkdir nanocorrect
2. tmux new -s nanocorrect

*convert .fastq to .fa*

4. more nanopore.all.fastq | awk '{if(NR%4==1) {printf(">%s\n",substr($0,2));} else if(NR%4==2) print;}' > nanopore.all.fa		

*run it*

5. make -f nanocorrect-overlap.make INPUT=../nanopore.all.fa NAME=corrected
6. python nanocorrect.py corrected all > corrected.fasta

##SPades 1st

**WD: /mnt/data3/lah/nanopore/nanocorrect2**

1. spades.py -1 harm1.fq -2 harm2.fq --nanopore corrected.fasta -t 8 -m 500 -o harmonia.nanopore2.spades --careful --only-assembler

#####restart
2. spades.py -1 harm1.fq -2 harm2.fq --nanopore corrected.fasta -t 8 -m 500 -o harmonia.nanopore2.spades --careful --only-assembler --continue
3. mv scaffolds.fasta 21.33.55.77.scaffolds.fasta
4. abyss-fac -e 665000000 21.33.55.77.scaffolds.fasta

		1634
**Still super low...could it be because there isn't much coverage? 



##Run nanocorrect on old nanopore data (so I can combine them?)
**WD: /mnt/data3/lah/nanopore/nanocorrect**

*convert .fastq to .fasta

1. more nanopore.harmonia.fastq | awk '{if(NR%4==1) {printf(">%s\n",substr($0,2));} else if(NR%4==2) print;}' > nanopore.harmonia.fasta 

1. make -f nanocorrect-overlap.make INPUT=nanopore.harmonia.fasta NAME=corrected 

		



	
					
