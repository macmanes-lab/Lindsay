#Useful commands

Counting number of reads from fastq file:

How I did it:
	
	grep @ harm1.fq | wc -l
	
		80000000
		
	grep @ harm2.fq | wc -l
	
		80000000
*This could not work becuase there are @ quality scores* 

How Matt does it:

	grep -c @HWI file.fq
	
		grep -c @HWI harm1.fq
			
			80000000
			
		grep -c @HWI harm2.fq
			80000000
			