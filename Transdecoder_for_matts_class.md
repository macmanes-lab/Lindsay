###WD: /mnt/data3/lah/mattsclass/transdecoder



#Running abyss-fac on raw trinity.fasta files

1. abyss-fac bless_norm_Trinity.fasta

		n=267314  n50=1892
		
2. abyss-fac no.norm.bless.trinity.fasta

		n=266291 n50=1913

3. abyss-fac p_eremicus_sga_with_norm_trinity.fasta

		n=163516 n50=1637
		
4. abyss-fac p_eremicus_sga_no_norm_trinity.fasta

		n=142188 n50=2082
		
		
##Running TransDecoder with files 

1. nohup TransDecoder -S --CPU 20 -t bless_norm_Trinity.fasta &