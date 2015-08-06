##4 additional RNA libraries
**Raw WD: /mnt/data3/macmanes/NYGC_August2015/raw_data**

**WD on my workspace: /mnt/data3/lah/adult_transcriptomes**

**pictures of bugs: /Users/lindsayhavens/Documents/Science/Ladybugs_2015/RNA --> cDNA 0129**

#####Bless (error correct)
#####Trinity
#####Transrate
#####Kallisto

1. mkdir adult_transcriptomes

		Description of bugs:
			30129- Orange/yellow spotless
			40129- yellow 21 spots
			70129- red orange, 19 spots
			80129 - yellow 21 spots 
			
			
##Bless
**WD:/mnt/data3/lah/adult_transcriptomes/bless** 

*30129*			

1. /share/bless/./bless -read1 ../30129_TAGCTT_BC6PR5ANXX_L008_001.R1.fastq -read2 ../30129_TAGCTT_BC6PR5ANXX_L008_001.R2.fastq -kmerlength 25 -verify -notrim -prefix 30129  

	 	 
     	 Checking input read files
    		 Number of reads           : 38710598
    		 Read length               : 125
    		 Max trimmed bases         : 62
    		 Quality score offset      : 33
    		 Quality score threshold   : 23
    		 Low quality score threhold: 15
    		 Max allowed Ns            : 12
     		 Checking input read files: done
			 Max allowed Ns            : 12

*40129*   

1. /share/bless/./bless -read1 ../40129_GGCTAC_BC6PR5ANXX_L008_001.R1.fastq -read2 ../40129_GGCTAC_BC6PR5ANXX_L008_001.R2.fastq -kmerlength 25 -verify -notrim -prefix 40129  


		Checking input read files
    		 Number of reads           : 31894166
    		 Read length               : 125
   			 Max trimmed bases         : 62
    		 Quality score offset      : 33
    		 Quality score threshold   : 18
   			 Low quality score threhold: 15
     		 Max allowed Ns            : 12
     		 Checking input read files: done

*70129*

1. /share/bless/./bless -read1 ../70129_CTTGTA_BC6PR5ANXX_L008_001.R1.fastq -read2 ../70129_CTTGTA_BC6PR5ANXX_L008_001.R2.fastq -kmerlength 25 -verify -notrim -prefix 70129 

		Checking input read files
     		Number of reads           : 100133196
     		Read length               : 125
     		Max trimmed bases         : 62
     		Quality score offset      : 33
    		Quality score threshold   : 23
     		Low quality score threhold: 15
     		Max allowed Ns            : 12
     		Checking input read files: done


*80129*

1. /share/bless/./bless -read1 ../80129_AGTCAA_BC6PR5ANXX_L008_001.R1.fastq -read2 ../80129_AGTCAA_BC6PR5ANXX_L008_001.R2.fastq -kmerlength 25 -verify -notrim -prefix 80129 

		Checking input read files
     		Number of reads           : 106141522
     		Read length               : 125
     		Max trimmed bases         : 62
    		Quality score offset      : 33
     		Quality score threshold   : 23
     		Low quality score threhold: 15
     		Max allowed Ns            : 12
     		Checking input read files: done
