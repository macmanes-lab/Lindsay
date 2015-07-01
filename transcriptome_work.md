#Transcriptome work
##Game plan:
#### 1. kallisto 
####2. blast to tribolium
####3. PANTHER (gene ontology)
####4. HMMER3 (conserved protein domains contained in the dataset using Pfam database)
####5. Transdecoder (putative coding sequences)

June 22, 2015
###kallisto

**WD: /mnt/data3/lah/transcriptome_work/kallisto**

1. make ghost files of transcriptome work 	

	ln -s /mnt/data3/lah/bless/nontrimmed.adult.bless/trinity.with.no.norm/adult.notrim.bless.nonorm.trinity.fasta/adult.notrim.bless.nonorm.trinity.fasta
	
	ln -s /mnt/data3/lah/bless/nontrimmed.larva.bless/larva.notrim.bless.nonorm.trinity.fasta/larva.notrim.bless.nonorm.trinity.fasta
	
2. tmux new -s kallisto

###Adult

3. kallisto index -i adult.idx adult.notrim.bless.nonorm.trinity.fasta
4. kallisto quant -i adult.idx -o adult.output --plaintext no.trimmed.adult.1.corrected.fastq no.trimmed.adult.2.corrected.fastq 
 
###Larva

5. kallisto index -i larva.idx larva.notrim.bless.nonorm.trinity.fasta  
6. kallisto quant -i larva.idx -o larva.output --plaintext no.trimmed.larva.1.corrected.fastq no.trimmed.larva.2.corrected.fastq 

###Blast high abundance contigs with uniprot database

**WD: /mnt/data3/lah/transcriptome_work/kallisto/blast**

1. Grep 20 best contigs (based on tpm of abundance.txt)from adult.notrim.bless.nonorm.trinity.fasta file


		Put into adultdb
2. Grep 20 best contigs (based on tpm of abundance.txt)from larva.notrim.bless.nonorm.trinity.fasta file	


		Put into larvadb
3. makeblastdb -in uniprot_sprot.fasta -out uniprot -dbtype prot
4. tmux new -s blast
5. blastx -db uniprot -query adultdb -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 5 > adult_txn_blast
6. blastx -db uniprot -query larvadb -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 5 > larva_txn_blast

		**Nothing super intersting here...just a lot of myosin and cytocrome c sequences

June 25, 2015	
###Blast adult transcriptome with tribolium database
**WD: /mnt/data3/lah/transcriptome_work/tribolium_blast/adult**		

1. ln -s /mnt/data3/lah/cpg_blast/tribolium.protein.fa
2. tmux at -t blast
3. makeblastdb -in tribolium.protein.fa -out tribolium -dbtype prot
3. blastx -db tribolium -query ../adult.notrim.bless.nonorm.trinity.fasta -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > adult_txn_tribolium_blast
4. **Find number of unique hits** cat adult_txn_tribolium_blast |awk '{print $1}' | uniq | wc -l

			22981
5. cat adult_txn_tribolium_blast | sort -gk5 | awk '{ print $1 }' | sort | uniq > adult_unique_evalue_hits_just_contigs
6. cat adult_txn_tribolium_blast | sort -gk5  > adult_top_evalue_hits
7. *Take tribolium protein ID from top 20 hits. Consider unique contig , best % identity (if tie, keep both), evalue grep back to the tribolium.protein.fa* 
8. nano adult_headers_to_grep
9. grep -f headers_to_grep tribolium.protein.fa > adult_tribolium_proteins_top20
			
			Nothing super interesting
10. cat adult_txn_tribolium_blast | sort -gk5 | awk '{ print $2 }' | sort | uniq > adult_unique_evalue_hits_just_trib.proteins
11. tmux new -s grep
11. grep -f adult_unique_evalue_hits_just_trib.proteins tribolium.protein.fa > adult_tribolium_proteins_all			

#
###Blast larva transcriptomes with tribolium database

**WD:/mnt/data3/lah/transcriptome_work/tribolium_blast/larva**

1. blastx -db tribolium -query ../larva.notrim.bless.nonorm.trinity.fasta -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > larva_txn_tribolium_blast
2. cat larva_txn_tribolium_blast | awk '{print $1}' | uniq | wc -l

			23764
3. cat larva_txn_tribolium_blast | sort -gk5 > larva_top_evalue_hits
4. nano larva_headers_to_grep	

			Interesting:
			gi|91084419|ref|XP_967907.1| PREDICTED: protein Red [Tribolium castaneum]
			This protein matches to contig # c10191_g1_i1

5.  grep c10191_g1_i1 larva_txn_tribolium_blast | wc -l 
			
			1  
					
6. grep 91084419 larva_txn_tribolium_blast 

			1 hit
			 	
			c10191_g1_i1    gi|91084419|ref|XP_967907.1|    78.99   476     0.0
7. grep -A50 c10191_g1_i1 larva.notrim.bless.nonorm.trinity.fasta
8. Blast contig 
9. blastn hit to Aplysia californica (sea slug)red-like protein 
10.tblastx hit to tribolium red protein as well as multiple other red proteins
		
			From megachile rotundata (bee)
				 Harpegnathos saltator (ant)
				 Culex quinquefasciatus (mosquito)
				 Solenopsis invicta (ant)
					and more!		
					
###Blast against Aphid to check for contamination
*nucleotide*

1. wget https://www.aphidbase.com/aphidbase/content/download/3246/33646/file/assembly2_scaffolds.fasta.bz2	
2. bzip2 -dk assembly2_scaffolds.fasta.bz2 
3. tmux at -t blast


4. blastn -db aphid -query ../adult.notrim.bless.nonorm.trinity.fasta -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > adult_aphid_blast
5. cat adult_aphid_blast |awk '{print $1}' | uniq | wc -l 

			279
6. Top 100 nucleotide hits based on percent identity
7. nano aphid_nucleotides
8. grep -f aphid_nucleotides assembly2_scaffolds.fasta > protein_from_blastn 
9. Nothing useful		
	
5. blastn -db aphid -query ../larva.notrim.bless.nonorm.trinity.fasta -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > larva_aphid_blast
6. cat larva_aphid_blast |awk '{print $1}' | uniq | wc -l 

			378
			
*protein*

5. wget https://www.aphidbase.com/aphidbase/content/download/3347/34150/file/aphidbase_2.1b_pep.fasta.bz2
6.  makeblastdb -in aphidbase_2.1b_pep.fasta -out aphid_protein -dbtype prot
7.  tmux new -s blast_protein
7.  blastx -db aphid_protein -query ../adult.notrim.bless.nonorm.trinity.fasta -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > adult_aphid_protein_blast
8.  cat adult_aphid_protein_blast | awk '{print$1}' | uniq | wc -l
		
			21009 
			
			**okay, but they are both insects so proteins will be conserved...what proteins are they?**		

9. grab top 100...only telling me that they are scaffolds from assembly			


###Rerunning these with larva and adult combined 
1. cat adult.notrim.bless.nonorm.trinity.fasta  larva.notrim.bless.nonorm.trinity.fasta > adult.larva.notrim.bless.nonorm.trinity.fasta
2. tmux new -s cd_hit
3. cd-hit-est -i adult.larva.notrim.bless.nonorm.trinity.fasta -o cd_hit_filtered_combined_file.fasta 			
**Nevermind..use transrate to do this**



#*Start over w/ merged and transrate corrected data 

###1. Transrate w/ merge function  
**WD:/mnt/data3/lah/transcriptome_work/transrate**

1. You use the files that you used for the assembly...these are the corrected files for me
2. Still in cd_hit tmux window
3. merge left adult and larva together and right adult and larva together 
4. cat no.trimmed.adult.1.corrected.fastq no.trimmed.larva.1.corrected.fastq > adult.larva.1.corrected.fastq
5. cat no.trimmed.adult.2.corrected.fastq no.trimmed.larva.2.corrected.fastq > adult.larva.2.corrected.fastq
6. transrate --merge-assemblies=merge.fasta --assembly ../adult.notrim.bless.nonorm.trinity.fasta ../larva.notrim.bless.nonorm.trinity.fasta --left adult.larva.1.corrected.fastq --right adult.larva.2.corrected.fastq  

							Contig metrics:
							
		[ INFO] 2015-07-01 09:53:12 : -----------------------------------
		[ INFO] 2015-07-01 09:53:12 : n seqs                        81986
		[ INFO] 2015-07-01 09:53:12 : smallest                        200
		[ INFO] 2015-07-01 09:53:12 : largest                       21577
		[ INFO] 2015-07-01 09:53:12 : n bases                    75761011
		[ INFO] 2015-07-01 09:53:12 : mean len                     924.07
		[ INFO] 2015-07-01 09:53:12 : n under 200                       0
		[ INFO] 2015-07-01 09:53:12 : n over 1k                     20777
		[ INFO] 2015-07-01 09:53:12 : n over 10k                       94
		[ INFO] 2015-07-01 09:53:12 : n with orf                    19952
		[ INFO] 2015-07-01 09:53:12 : mean orf percent              54.83
		[ INFO] 2015-07-01 09:53:12 : n90                             312
		[ INFO] 2015-07-01 09:53:12 : n70                             956
		[ INFO] 2015-07-01 09:53:12 : n50                            1979
		[ INFO] 2015-07-01 09:53:12 : n30                            3262
		[ INFO] 2015-07-01 09:53:12 : n10                            5634
		[ INFO] 2015-07-01 09:53:12 : gc                             0.36
		[ INFO] 2015-07-01 09:53:12 : gc skew                         0.0
		[ INFO] 2015-07-01 09:53:12 : at skew                         0.0
		[ INFO] 2015-07-01 09:53:12 : cpg ratio                      1.67
		[ INFO] 2015-07-01 09:53:12 : bases n                           0
		[ INFO] 2015-07-01 09:53:12 : proportion n                    0.0
		[ INFO] 2015-07-01 09:53:12 : linguistic complexity          0.15
		[ INFO] 2015-07-01 09:53:12 : Contig metrics done in 19 seconds
		
		 						Read mapping metrics:
		 						
		[ INFO] 2015-07-01 11:34:59 : -----------------------------------
		[ INFO] 2015-07-01 11:34:59 : fragments                 125489529
		[ INFO] 2015-07-01 11:34:59 : fragments mapped          115787433
		[ INFO] 2015-07-01 11:34:59 : p fragments mapped             0.92
		[ INFO] 2015-07-01 11:34:59 : good mappings              86554402
		[ INFO] 2015-07-01 11:34:59 : p good mapping                 0.69
		[ INFO] 2015-07-01 11:34:59 : bad mappings               29233031
		[ INFO] 2015-07-01 11:34:59 : potential bridges             24381
		[ INFO] 2015-07-01 11:34:59 : bases uncovered             8106044
		[ INFO] 2015-07-01 11:34:59 : p bases uncovered              0.11
		[ INFO] 2015-07-01 11:34:59 : contigs uncovbase             49713
		[ INFO] 2015-07-01 11:34:59 : p contigs uncovbase            0.61
		[ INFO] 2015-07-01 11:34:59 : contigs uncovered              9369
		[ INFO] 2015-07-01 11:34:59 : p contigs uncovered            0.11
		[ INFO] 2015-07-01 11:34:59 : contigs lowcovered            56278
		[ INFO] 2015-07-01 11:34:59 : p contigs lowcovered           0.69
		[ INFO] 2015-07-01 11:34:59 : contigs segmented              8693
		[ INFO] 2015-07-01 11:34:59 : p contigs segmented            0.11
		[ INFO] 2015-07-01 11:34:59 : Read metrics done in 6107 seconds
		[ INFO] 2015-07-01 11:34:59 : No reference provided, skipping comparative diagnostics
		[ INFO] 2015-07-01 11:34:59 : TRANSRATE ASSEMBLY SCORE     0.1539
		[ INFO] 2015-07-01 11:34:59 : -----------------------------------
		[ INFO] 2015-07-01 11:34:59 : TRANSRATE OPTIMAL SCORE      0.2717
		[ INFO] 2015-07-01 11:34:59 : TRANSRATE OPTIMAL CUTOFF     0.0543
		[ INFO] 2015-07-01 11:34:59 : good contigs                  68176
		[ INFO] 2015-07-01 11:34:59 : p good contigs                 0.83
		[ INFO] 2015-07-01 11:34:59 : Writing contig metrics for each contig to transrate_merge.fasta_contigs.csv
		[ INFO] 2015-07-01 11:35:22 : Writing analysis results to transrate_assemblies.csv
		
7. mv good.merge.fasta larva.adult.transrate.good.fasta

###kalisto		
**WD: /mnt/data3/lah/transcriptome_work/kallisto/adult.larva.output**

1. ln -s /mnt/data3/lah/transcriptome_work/transrate/larva.adult.transrate.good.fasta
2. kallisto index -i larva.adult.idx larva.adult.transrate.good.fasta 
3. kallisto quant -i larva.adult.idx -o larva.adult --plaintext adult.larva.1.corrected.fastq adult.larva.2.corrected.fastq 