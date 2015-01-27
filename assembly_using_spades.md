#Assembly using SPAdes
**Doing this because low NG50 value with ABySS ~5500**


A . Try to run spades using the error corrector that is built in.

*May not work because it can only handle 2 billion characters or 32 bit and we have a 64 bit computer -- will fail within 5 hours. Check back at 3*

1. tmux new -s spades

		spades.py -1 harm1.fq -2 harm2.fq -t 24 -m 500 -o harmonia.spades --careful 
		
		-1 forward paired-end read
		-2 reverse paired-end read
		-t threads 
		-m memory (chose 500 Gb)
		-o output
		--careful reduce number of mismatches 
		
		*note I let SPAdes choose the kmer size 