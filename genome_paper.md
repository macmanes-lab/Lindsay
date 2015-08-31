##Fastqc on Illumina data (only did preqc originally)
**WD: /mnt/data3/lah/preqc/fastqc**

	fastqc seqfile1 seqfile2 .. seqfileN

    fastqc [-o output dir] [--(no)extract] [-f fastq|bam|sam] 
           [-c contaminant file] seqfile1 .. seqfileN
1. fastqc -f fastq ../harm1.fq ../harm2.fq 
##Bless error correction (done previously) 
	*alternative is bfc, but since I did this already going to use this*
	
	**WD:/mnt/data3/lah/bless/nontrimmed.genome.bless**
	
	1.  nohup bless -read1 ../harm1.fq -read2 ../harm2.fq -prefix no.trimmed -kmerlength 25 -notrim -verify &
		
		
			Parsing arguments is finished
    		 1st Read File Name         : ../harm1.fq
   	  		 2nd Read File Name         : ../harm2.fq
    		 Log File Name              : no.trimmed.genome.log
   			 K-mer Length               : 25
     		 Target False Positive Prob.: 0.001
     		 Random Seed                : 0
    		 K-mer Occurence Threshold  : Not specified
    		 Number of Clusters         : 100
    		 Read extension amount      : 5
    		 No output read write       : Off
    		 Removing false positives   : On
    		 Load existing BF data      : Off
    		 No trim reads              : On

			Checking input read files
    		 Number of reads           : 160000000
    		 Read length               : 151
     		 Max trimmed bases         : 75
   	 		 Quality score offset      : 33
   	 		 Quality score threshold   : 27
     		 Low quality score threhold: 2
     		 Max allowed Ns            : 15
   	 		 Checking input read files: done

			Counting the number of k-mers
    		 k-mer occurrence threshold   : 8
    		 Number of unique k-mers      : 952944994
    		 Number of unique solid k-mers: 420557403
    		 Counting the number of k-mers: done

	2. move these files to MaSuRCA folder: /mnt/data3/lah/genome_paper/masurca
		
##MaSuRCA (include nanocorrected- nanopore data here)
**WD: /mnt/data3/lah/genome_paper/masurca**

*this will make super reads for Illumina*

		"The aim is to create a set of super-reads that contains all of the sequence information present in the original reads despite the fact that there are far fewer super-reads than original read" (The MaSuRCA genome assembler: Zimin et al, 2013)
		
		http://www.genome.umd.edu/docs/MaSuRCA_QuickStartGuide.pdf
		
1. ln -s /mnt/data3/lah/nanopore/nanocorrect/nanocorrect.fasta
2. ln -s /mnt/data3/lah/nanopore/nanocorrect2/nanocorrect2.fasta
3. Have to convert these to fastq

			python /share/ectools/fastaToFastq.py nanocorrect.fasta > nanocorrect.fastq
			python /share/ectools/fastaToFastq.py nanocorrect2.fasta > nanocorrect2.fastq

*convert to CA*
			
4. fastqToCA -libraryname nanocorrect -technology pacbio-corrected -reads nanocorrect.fastq > nanocorrect_real.frg
5. ffastqToCA -libraryname nanocorrect -technology pacbio-corrected -reads nanocorrect2.fastq > nanocorrect2_real.frg	
6. /share/MaSuRCA-3.1.0beta/bin/masurca congfig.file.txt
7. ./assemble.sh
8. Convert superReadSequences.fasta to fastq

		python /share/ectools/fastaToFastq.py superReadSequences.fasta > superReadSequences.fastq
9. Convert fastq to .frg
	 	
	 	fastqToCA -libraryname superreads -technology sanger -reads superReadSequences.fastq > superReadSequences_real.frg

##Throw super-reads as well as the nanopore data into wgs
**WD: /mnt/data3/lah/genome_paper/wgs**
1. runCA -d wgs1 -p harmonia -s spec_file