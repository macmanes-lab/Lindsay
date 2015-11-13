#Optimize genome w/ transcriptome
####1. blat
####2. L_RNA scaffolder
		
		V1 genome
####3. BUSCO
_________________________________		
####1. Rcorrector
####2. Bwa to map corrected reads to v1 genome
####3. Samtools merge
####4. BESST.RNA

		V2 Genome	
####5. Busco			


#Blat
**WD:/mnt/data3/lah/better_genome**

#####Genome

Using trimmed,khmer normed, bless error corrected abyss file

**OWD: /mnt/data3/lah/abyss/trimmed.norm.bless.error.corrected.OPTIMAL/k121** 

#####Transcriptome
using vsearch merged, transrate improved transcriptome 
 **OWD:/mnt/data3/lah/transcriptome_work/transrate/vsearch_transrate**
good.unique_headers_adult.larva.centroid.trinity.fasta

	End of file reading 4 bytes
What I've tried:
		
		blat -noHead -t=dna /mnt/data3/lah/abyss/trimmed.norm.bless.error.corrected.OPTIMAL/k121/k121-scaffolds.fa -q=rna /mnt/data3/lah/transcriptome_work/transrate/vsearch_transrate/good.unique_headers_adult.larva.centroid.trinity.fasta output.psl
		
		blat -noHead -t=dna k121-scaffolds.fa -q=rna good.unique_headers_adult.larva.centroid.trinity.fasta output.psl
		
		blat -noHead -t=dna k121-scaffolds.fa -q=rna good.unique_headers_adult.larva.centroid.trinity.fasta harmonia.psl
		
		blat -t=dna k121-scaffolds.fa -q=rna good.unique_headers_adult.larva.centroid.trinity.fasta output.psl
		
		blat -noHead k121-scaffolds.fa good.unique_headers_adult.larva.centroid.trinity.fasta output.psl
		
		blat -noHead k121-scaffolds.fa good.unique_headers_adult.larva.centroid.trinity.fasta harmonia.psl	
		
###transcriptome file was empty

		figured this out bc used abyss-fac on it
		
####transcriptome 
**OWD: /mnt/data3/lah/transcriptome_work/vsearch**

#Blat
blat -noHead k121-scaffolds.fa adult.larva.centroid.trinity.fasta harmonia.psl

		Loaded 831343170 letters in 515159 sequences
		Searched 105315076 bases in 130500 sequences

#L_RNA_scaffolder.sh
**WD: /mnt/data3/lah/better_genome**

L_RNA_scaffolder.sh -d /share/L_RNA_scaffolder -i harmonia.psl -j k121-scaffolds.fa

	abyss-fac L_RNA_scaffolder.fasta 
	N50= 4163

	abyss-fac k121-scaffolds.fa
	N50= 4109
	
	abyss-fac -e 830000000 L_RNA_scaffolder.fasta
	NG50 = 3908
	
BUSCO: 
	
#bwa
1. bwa index -p harmonia ../L_RNA_scaffolder.fasta

		seqtk mergepe \
		/mnt/data3/lah/adult_transcriptomes/rcorrector/30129/30129_TAGCTT_BC6PR5ANXX_L008_001.R1.cor.fq \
		/mnt/data3/lah/adult_transcriptomes/rcorrector/30129/30129_TAGCTT_BC6PR5ANXX_L008_001.R1.cor.fq \
		| skewer -Q 2 -t 10 -x /share/trinityrnaseq/trinity-plugins/Trimmomatic/adapters/TruSeq3-PE-2.fa - -1 \
		| extract-paired-reads.py -p - -s /dev/null - \
		| bwa mem -p -t 10 harmonia - \
		| samtools view -T . -bu - \
		| samtools sort -l 0 -O bam -T tmp -@ 15 -m 22G -o 30129.harmonia.bam -
		
#merge 
samtools merge all.bam *.bam	
samtools index all.bam

#BESST_RNA
1. python /share/BESST_RNA/src/Main.py 1 -c ../L_RNA_scaffolder.fasta -f all.bam -e 3 -T 50000 -k 500 -d 1 -z 1000 -o scaffold_2_harmonia/

		abyss-fac -e 830000000 Scaffolds-pass1.fa
		NG50 4040
		
		
# Besst_RNA isn't working
- think it might be the subprocess("") command?
	- even though this works for bwa and samtools. it's pulling the file open, but is saying:
	
		  File "/share/BESST_RNA/src/CreateGraph.py", line 352, in 		CalculateMeanCoverage
    		mean_cov = sum(filtered_list) / n
		ZeroDivisionError: float division by zero

- Tried running it w/o subproces..it still failed

			
			Ran w/ subprocess...there was an update 20 days ago that we didn't have!! 

#making play dataset:

**WD: /mnt/data3/lah/better_genome/besst_rna/baby_set**

seqtk sample -s1040 harm1.fq 10000 > subsamp_1.fastq

seqtk sample -s1040 harm2.fq 10000 > subsamp_2.fastq

#sed
- getting rid of blank lines

		sed -i '/^$/d' one.fasta 
		(^ = beginning $ = end)
		
		
		
#besst_rna with 

/mnt/data3/lah/better_genome/bwa/scaffold_3_harmonia/pass1

		N50 = 4115		
		
		
#Completed 4 iterations:

abyss-fac -e 812000000 Scaffolds-pass1.fa :

1st iteration

		NG50 - 4211
		
2nd iteration - 	
			
		NG50 - 3900
		
3rd iteration - 
		
		NG50 - 3753

4th iteratiion				
		
		NG50 - 3621
		
		
#why are these numbers so low?
**WD:/mnt/data3/lah/automate4/iter_1/pass1**

- bwa mem to map final transcriptome against an index containing my scaffold file 

**Transcriptome:** 

/mnt/data3/lah/transcriptome_work/transrate/good.good.unique_headers_adult.larva.centroid.trinity.fasta

**Scaffold file**

/mnt/data3/lah/automate4/iter_1/pass1/Scaffolds-pass1.fa

**fasta2fastq**
1. curl -L http://www.cbcb.umd.edu/software/PBcR/data/convertFastaAndQualToFastq.jar > convertFastaAndQualToFastq.jar
2. nano fq2fa.sh

	#! /bin/bash

	for i in `ls *fasta`; 
    	do java -jar convertFastaAndQualToFastq.jar $i > $i.fq; 
    	done
**bwa**

1. bwa index Scaffolds-pass1.fa    
2. bwa mem Scaffolds-pass1.fa good.good.unique_headers_adult.larva.centroid.trinity.fasta.fq


#Analyze 
**WD: automate4**

1. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o iter1.eukaryota -f -in Scaffolds-pass1.fa -l /mnt/data3/lah/b
usco/eukaryota/


		Summarized benchmarks in BUSCO notation:
			C:49%[D:21%],F:11%,M:38%,n:429

		Representing:
			213	Complete Single-Copy BUSCOs
			91	Complete Duplicated BUSCOs
			50	Fragmented BUSCOs
			166	Missing BUSCOs
			429	Total BUSCO groups searched
	- lots of duplicated (so maybe BESST-RNA wasn't the best one to use)		
			
2. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o iter1.arthropoda -f -in Scaffolds-pass1.fa -l /mnt/data3/lah/busco/arthropoda/	


#looking at L-scaffolder on aws
**WD:/home/ubuntu**
ubuntu@ec2-52-26-10-239.us-west-2.compute.amazonaws.com:/home/ubuntu/

1. python3 BUSCO_v1.1b1/BUSCO_v1.1b1.py -o l_scaffold_arthropoda -in L_RNA_scaffolder.fasta -l BUSCO_v1.1b1/arthropoda/

		#BUSCO was run in mode: genome

		Summarized benchmarks in BUSCO notation:
			C:57%[D:22%],F:24%,M:17%,n:2675

		Representing:
			1547	Complete Single-Copy BUSCOs
			601	Complete Duplicated BUSCOs
			658	Fragmented BUSCOs
			470	Missing BUSCOs
			2675	Total BUSCO groups searched


2. python3 BUSCO_v1.1b1/BUSCO_v1.1b1.py -o -f l_scaffold_eukaryota -in L_RNA_scaffolder.fasta -l BUSCO_v1.1b1/eukaryota/


		#BUSCO was run in mode: genome

		Summarized benchmarks in BUSCO notation:
			C:59%[D:27%],F:19%,M:20%,n:429

		Representing:
			256	Complete Single-Copy BUSCOs
			116	Complete Duplicated BUSCOs
			83	Fragmented BUSCOs
			90	Missing BUSCOs
			429	Total BUSCO groups searched
