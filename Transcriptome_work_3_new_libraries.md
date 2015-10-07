##4 additional RNA libraries
**Raw WD: /mnt/data3/macmanes/NYGC_August2015/raw_data**

**WD on my workspace: /mnt/data3/lah/adult_transcriptomes**

**pictures of bugs: /Users/lindsayhavens/Documents/Science/Ladybugs_2015/RNA --> cDNA 0129**

#####SEECER-0.1.3 (error correct)
		Use SEECER bc I have more than 50,000,000 reads 
#####Quality and adapter trim (trimmomatic)
#####map reads to reference -- bwa

		see how many map...if 90% map we know reference is good (vsearch merged)
		if 70% map...improve reference 
		
#####Kallisto



##Description of bugs

		Description of bugs:
			30129- Orange/yellow spotless
			40129- yellow 21 spots
			70129- red orange, 19 spots
			80129 - yellow 21 spots 
		
			
##Bless --killed this bc SEECER is better, but got number of reads and read length


*30129*			

	 	 
     	 Checking input read files
    		 Number of reads           : 38710598
    		 Read length               : 125
    	

*40129*   



		Checking input read files
    		 Number of reads           : 31894166
    		 Read length               : 125
   			

*70129*


		Checking input read files
     		Number of reads           : 100133196
     		Read length               : 125
     	

*80129*

		Checking input read files
     		Number of reads           : 106141522
     		Read length               : 125
     		
     		
##SEECER (can only run 1 at a time)
**WD: /mnt/data3/lah/adult_transcriptomes/seecer**
	
Using this b/c of sugggestions made in optimizzing error correction of RNAseq reads 

* Use default kmer length of 17

*30129*  		
 
1. seecer 30129_TAGCTT_BC6PR5ANXX_L008_001.R1.fastq 30129_TAGCTT_BC6PR5ANXX_L008_001.R2.fastq

*40129*

1. seecer 40129_GGCTAC_BC6PR5ANXX_L008_001.R1.fastq 40129_GGCTAC_BC6PR5ANXX_L008_001.R2.fastq

*70129*

1. seecer 70129_CTTGTA_BC6PR5ANXX_L008_001.R1.fastq 70129_CTTGTA_BC6PR5ANXX_L008_001.R2.fastq 

*80129*

1. seecer 80129_AGTCAA_BC6PR5ANXX_L008_001.R1.fastq 80129_AGTCAA_BC6PR5ANXX_L008_001.R2.fastq  	

##BWA
*30129*

1. bwa index -p bwa_index corrected_reads.fa
2. bwa mem bwa_index corrected_reads.fa | samtools view -Sb - > test.bam
3. mv test.bam 30129.bam

*40129*

1. bwa index -p bwa_index corrected_reads.fa
2. bwa mem bwa_index corrected_reads.fa | samtools view -Sb - > 40129.bam

	
	
#rcorrector
**WD: /mnt/data3/lah/adult_transcriptomes/rcorrector**

*30129*

perl /share/Rcorrector/run_rcorrector.pl -1 ../30129_TAGCTT_BC6PR5ANXX_L008_001.R1.fastq -2 ../30129_TAGCTT_BC6PR5ANXX_L008_001.R2.fastq -t 10

	Processed 38710598 reads
        Corrected 11568621 bases.
        
*40129*
perl /share/Rcorrector/run_rcorrector.pl -1 ../ 40129_GGCTAC_BC6PR5ANXX_L008_001.R1.fastq -2 ../ 0129_GGCTAC_BC6PR5ANXX_L008_001.R2.fastq -t 10
	
	Processed 31894166 reads
        Corrected 9562341 bases.
        
*70129*  
perl /share/Rcorrector/run_rcorrector.pl -1 ../70129_CTTGTA_BC6PR5ANXX_L008_001.R1.fastq ../70129_CTTGTA_BC6PR5ANXX_L008_001.R2.fastq -t 10  
		
	Processed 100133196 reads
        Corrected 28495607 bases.
*80129*
perl /share/Rcorrector/run_rcorrector.pl -1 ../80129_AGTCAA_BC6PR5ANXX_L008_001.R1.fastq -2 ../80129_AGTCAA_BC6PR5ANXX_L008_001.R2.fastq -t 10  
	
	Processed 106141522 reads
        	Corrected 31009879 bases.
        	
blat 
-scaffolds 


l_rna_scaffolder
 - transcriptome to genome
 
 -maps reads back to         	