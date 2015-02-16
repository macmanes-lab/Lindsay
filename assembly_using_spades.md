#Assembly using SPAdes 
**Doing this because low NG50 value with ABySS ~5500**

WD:/mnt/data3/lah/spades

**1st try to run spades using the error corrector that is built in.**

*May not work because it can only handle 2 billion characters or 32 bit and we have a 64 bit computer -- will fail within 5 hours. Check back at 3*
		
		Didn't fail!

1.) tmux new -s spades
	
	spades.py -1 harm1.fq -2 harm2.fq -t 24 -m 500 -o harmonia.spades --careful 
		
		-1 forward paired-end read
		-2 reverse paired-end read
		-t threads 
		-m memory (chose 500 Gb)
		-o output
		--careful reduce number of mismatches 
		
**I let SPAdes choose the kmer size** 
			
	it chose a kmer size of 21, 33, 66 and 77 because estimated read length (151) is equal to or greater than 150 
	

2.) Estimate N50 for K21, K33, K55, K77

*For kmer 21*

WD:/mnt/data3/lah/spades/harmonia.spade/K21


1. abyss-fac -e 665000000 final_contigs.fasta

		N50-684
		NG50-500

*for kmer 33*

WD:/mnt/data3/lah/spades/harmonia.spades/K3


1. abyss-fac -e 665000000 final_contigs.fasta

		N50-951
		NG50-500
		
*for kmer 55**

WD:	/mnt/data3/lah/spades/harmonia.spades/K55

1. abyss-fac -e 665000000 final_contigs.fasta

		N50-1020
		NG50-500	
		
*for kmer 77*

WD:/mnt/data3/lah/spades/harmonia.spades/K77

1. abyss-fac -e 665000000 final_contigs.fasta

		N50-2099
		NG50-1513
2. abyss-fac -e 665000000 scaffolds.fasta -- this is the only one with scaffolds file

		N50-2148
		NG50-1543

**Low N50 values!**

##Re-Run spades with kmer values 93,101,111,121 

WD:/mnt/data3/lah/spades

1.) tmux new -s spades_with_big_kmer

		spades.py -1 harm1.fq -2 harm2.fq -t 24 -k 93,101,111,121 -m 500 -o harmonia.spades_large_kmer --careful 
		
		
2.) Davinci had to go down, restart

tmux new -s spades_with_big_kmer		

		spades.py -1 harm1.fq -2 harm2.fq -t 24 -k 93,101,111,121 -m 500 -o harmonia.spades_large_kmer --careful --continue
			
