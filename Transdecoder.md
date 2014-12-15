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

**TransDecoder on bless with khmer Trinity fasta**

1. nohup TransDecoder -S --CPU 20 -t bless_norm_Trinity.fasta &
2. mkdir bless.norm.transdecoder
3. mv bless_norm_Trinity.* bless.norm.transdecoder/
4. cd bless.norm.transdecoder
5. grep -c "complete" bless_norm_Trinity.fasta.transdecoder.pep
		
		14546

**TransDecoder on bless with no khmer Trinity fasta**

1. nohup TransDecoder -S --CPU 20 -t no.norm.bless.trinity.fasta &
2.  mkdir bless.no.norm.transdecoder
3.  mv no.norm.bless.trinity.* bless.no.norm.transdecoder/
4.  cd bless.no.norm.transdecoder
5.  grep -c "complete" no.norm.bless.trinity.fasta.transdecoder.pep

		14502

**TransDecoder on SGA with khmer Trinity fasta**

1. nohup TransDecoder -S --CPU 20 -t p_eremicus_sga_with_norm_trinity.fasta &
2. mkdir sga.norm.transdecoder
3. mv p_eremicus_sga_with_norm_trinity.* sga.norm.transdecoder/
4. cd sga.norm.transdecoder
5. grep -c "complete" p_eremicus_sga_with_norm_trinity.fasta.transdecoder.pep

		11249


**TransDecoder on SGA with no khmer Trinity fasta**

1. nohup TransDecoder -S --CPU 20 -t p_eremicus_sga_no_norm_trinity.fasta &
2. mkdir sga.no.norm.transdecoder
3. mv p_eremicus_sga_no_norm_trinity.* sga.no.norm.transdecoder/
4. cd sga.no.norm.transdecoder
5. grep -c "complete" p_eremicus_sga_no_norm_trinity.fasta.transdecoder.pep

		11394