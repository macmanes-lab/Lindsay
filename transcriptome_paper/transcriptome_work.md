#Transcriptome work
##Game plan:
####1. Transrate
#### 2. kallisto 
####3. blast to tribolium/aphid 
####4. PANTHER (gene ontology)
####5. Transdecoder (putative coding sequences)
####6. Hmmer?

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
July 1, 2015
					
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

**score was bad, didn't include a comma so it may not be merged**

1. transrate --merge-assemblies=merge.fasta --assembly ../adult.notrim.bless.nonorm.trinity.fasta,../larva.notrim.bless.nonorm.trinity.fasta --left adult.larva.1.corrected.fastq --right adult.larva.2.corrected.fastq 

	-----------------------------------
		[ INFO] 2015-07-01 13:44:54 : n seqs                       150862
		[ INFO] 2015-07-01 13:44:54 : smallest                        200
		[ INFO] 2015-07-01 13:44:54 : largest                       21577
		[ INFO] 2015-07-01 13:44:54 : n bases                   131191876
		[ INFO] 2015-07-01 13:44:54 : mean len                     869.62
		[ INFO] 2015-07-01 13:44:54 : n under 200                       0
		[ INFO] 2015-07-01 13:44:54 : n over 1k                     36919
		[ INFO] 2015-07-01 13:44:54 : n over 10k                      110
		[ INFO] 2015-07-01 13:44:54 : n with orf                    37806
		[ INFO] 2015-07-01 13:44:54 : mean orf percent              56.96
		[ INFO] 2015-07-01 13:44:54 : n90                             301
		[ INFO] 2015-07-01 13:44:54 : n70                             849
		[ INFO] 2015-07-01 13:44:54 : n50                            1778
		[ INFO] 2015-07-01 13:44:54 : n30                            2900
		[ INFO] 2015-07-01 13:44:54 : n10                            5078
		[ INFO] 2015-07-01 13:44:54 : gc                             0.36
		[ INFO] 2015-07-01 13:44:54 : gc skew                         0.0
		[ INFO] 2015-07-01 13:44:54 : at skew                         0.0
		[ INFO] 2015-07-01 13:44:54 : cpg ratio                      1.66
		[ INFO] 2015-07-01 13:44:54 : bases n                           0
		[ INFO] 2015-07-01 13:44:54 : proportion n                    0.0
		[ INFO] 2015-07-01 13:44:54 : linguistic complexity          0.15
		
		 Read mapping metrics: -----------------------------------
		[ INFO] 2015-07-01 16:21:31 : fragments                 125489529
		[ INFO] 2015-07-01 16:21:31 : fragments mapped          114116862
		[ INFO] 2015-07-01 16:21:31 : p fragments mapped             0.91
		[ INFO] 2015-07-01 16:21:31 : good mappings              87320928
		[ INFO] 2015-07-01 16:21:31 : p good mapping                  0.7
		[ INFO] 2015-07-01 16:21:31 : bad mappings               26795934
		[ INFO] 2015-07-01 16:21:31 : potential bridges             39488
		[ INFO] 2015-07-01 16:21:31 : bases uncovered            17171165
		[ INFO] 2015-07-01 16:21:31 : p bases uncovered              0.13
		[ INFO] 2015-07-01 16:21:31 : contigs uncovbase             96872
		[ INFO] 2015-07-01 16:21:31 : p contigs uncovbase            0.64
		[ INFO] 2015-07-01 16:21:31 : contigs uncovered             26406
		[ INFO] 2015-07-01 16:21:31 : p contigs uncovered            0.18
		[ INFO] 2015-07-01 16:21:31 : contigs lowcovered           111265
		[ INFO] 2015-07-01 16:21:31 : p contigs lowcovered           0.74
		[ INFO] 2015-07-01 16:21:31 : contigs segmented             14065
		[ INFO] 2015-07-01 16:21:31 : p contigs segmented            0.09
		[ INFO] 2015-07-01 16:21:31 : Read metrics done in 9397 seconds
		[ INFO] 2015-07-01 16:21:31 : No reference provided, skipping comparative diagnostics
		[ INFO] 2015-07-01 16:21:31 : TRANSRATE ASSEMBLY SCORE     0.1507
		[ INFO] 2015-07-01 16:21:31 : -----------------------------------
		[ INFO] 2015-07-01 16:21:31 : TRANSRATE OPTIMAL SCORE      0.2944
		[ INFO] 2015-07-01 16:21:31 : TRANSRATE OPTIMAL CUTOFF     0.0557
		[ INFO] 2015-07-01 16:21:31 : good contigs                 122298
		[ INFO] 2015-07-01 16:21:31 : p good contigs                 0.81

###Vsearch

**WD:/mnt/data3/lah/transcriptome_work/vsearch**

- transrate merge is experimental, so running vsearch on my concatenated trinity files and  then rerunning transrate to see the difference

1. tmux new -s vsearch_LH
2. vsearch --fasta_width 0 --threads 5 --id .99 --cons_truncate   
--cluster_fast ../adult.larva.notrim.bless.nonorm.trinity.fasta --strand both --centroid adult.larva.centroid.trinity.fasta

--con_truncate = do not ignore terminal gaps in MSA for consensus
-- reject is lower than .99
--centroid = output file name
--cluseter fast = input, but cluster these files


		Reading file ../adult.larva.notrim.bless.nonorm.trinity.fasta 100%  
		131191876 nt in 150862 seqs, min 200, max 21577, avg 870
		Indexing sequences 100%  
		Masking 100%
		Sorting by length 100%
		Counting unique k-mers 100%  
		Clustering 100%  
		Writing clusters 100%  
		Clusters: 130500 Size min 1, max 33, avg 1.2
		Singletons: 115057, 76.3% of seqs, 88.2% of clusters
		
		
###Transrate on vsearch		
**WD:/mnt/data3/lah/transcriptome_work/transrate/vsearch_transrate**

1. tmux new -s transrate
2. transrate -a unique_headers_adult.larva.centroid.trinity.fasta -l ../adult.larva.1.corrected.fastq -r ../adult.larva.2.corrected.fastq

**Because it is taking 2 trinity assemblies and merging them together, there are overlapping header identifiers...transrate doesn't like this**

**Rename the headers w/ 0,1,2,3 etc**

	awk '/^>/{print ">" ++i; next}{print}' < input.fa > output.fa

Search for something that begins w/ >, if you see it print that and 0, 1, 2, 3, etc
< input.fa is another way of saying cat | (pipe the input file to that command) 

3. awk '/^>/{print ">" ++i; next}{print}' < adult.larva.centroid.trinity.fasta  > unique_headers_adult.larva.centroid.trinity.fasta	
4. transrate -a unique_headers_adult.larva.centroid.trinity.fasta -l ../adult.larva.1.corrected.fastq -r ../adult.larva.2.corrected.fastq


		 --------------------Contig metrics:---------------
		[ INFO] 2015-07-03 08:09:20 : n seqs                       130500
		[ INFO] 2015-07-03 08:09:20 : smallest                        200
		[ INFO] 2015-07-03 08:09:20 : largest                       21577
		[ INFO] 2015-07-03 08:09:20 : n bases                   105315076
		[ INFO] 2015-07-03 08:09:20 : mean len                     807.01
		[ INFO] 2015-07-03 08:09:20 : n under 200                       0
		[ INFO] 2015-07-03 08:09:20 : n over 1k                     29227
		[ INFO] 2015-07-03 08:09:20 : n over 10k                       85
		[ INFO] 2015-07-03 08:09:20 : n with orf                    29837
		[ INFO] 2015-07-03 08:09:20 : mean orf percent              56.19
		[ INFO] 2015-07-03 08:09:20 : n90                             287
		[ INFO] 2015-07-03 08:09:20 : n70                             728
		[ INFO] 2015-07-03 08:09:20 : n50                            1578
		[ INFO] 2015-07-03 08:09:20 : n30                            2644
		[ INFO] 2015-07-03 08:09:20 : n10                            4752
		[ INFO] 2015-07-03 08:09:20 : gc                             0.36
		[ INFO] 2015-07-03 08:09:20 : gc skew                         0.0
		[ INFO] 2015-07-03 08:09:20 : at skew                         0.0
		[ INFO] 2015-07-03 08:09:20 : cpg ratio                      1.66
		[ INFO] 2015-07-03 08:09:20 : bases n                           0
		[ INFO] 2015-07-03 08:09:20 : proportion n                    0.0
		[ INFO] 2015-07-03 08:09:20 : linguistic complexity          0.14
		
		 -----------------------------------
		[ INFO] 2015-07-03 11:45:51 : fragments                 125489529
		[ INFO] 2015-07-03 11:45:51 : fragments mapped          117924573
		[ INFO] 2015-07-03 11:45:51 : p fragments mapped             0.94
		[ INFO] 2015-07-03 11:45:51 : good mappings              90812245
		[ INFO] 2015-07-03 11:45:51 : p good mapping                 0.72
		[ INFO] 2015-07-03 11:45:51 : bad mappings               27112328
		[ INFO] 2015-07-03 11:45:51 : potential bridges             23525
		[ INFO] 2015-07-03 11:45:51 : bases uncovered             8316387
		[ INFO] 2015-07-03 11:45:51 : p bases uncovered              0.08
		[ INFO] 2015-07-03 11:45:51 : contigs uncovbase             76324
		[ INFO] 2015-07-03 11:45:51 : p contigs uncovbase            0.58
		[ INFO] 2015-07-03 11:45:51 : contigs uncovered             16131
		[ INFO] 2015-07-03 11:45:51 : p contigs uncovered            0.12
		[ INFO] 2015-07-03 11:45:51 : contigs lowcovered            96791
		[ INFO] 2015-07-03 11:45:51 : p contigs lowcovered           0.74
		[ INFO] 2015-07-03 11:45:51 : contigs segmented             12393
		[ INFO] 2015-07-03 11:45:51 : p contigs segmented            0.09
		[ INFO] 2015-07-03 11:45:51 : Read metrics done in 5072 seconds
		[ INFO] 2015-07-03 11:45:51 : No reference provided, skipping comparative diagnostics
		[ INFO] 2015-07-03 11:45:51 : TRANSRATE ASSEMBLY SCORE     0.2182
		[ INFO] 2015-07-03 11:45:51 : -----------------------------------
		[ INFO] 2015-07-03 11:45:51 : TRANSRATE OPTIMAL SCORE       0.316
		[ INFO] 2015-07-03 11:45:51 : TRANSRATE OPTIMAL CUTOFF     0.0543
		[ INFO] 2015-07-03 11:45:51 : good contigs                 116514
		[ INFO] 2015-07-03 11:45:51 : p good contigs                 0.89

**This is better! Use the vsearch assembly for future work**

###kalisto	on merged files with merged read files
**WD: /mnt/data3/lah/transcriptome_work/kallisto/adult.larva.output**

1. ln -s /mnt/data3/lah/transcriptome_work/transrate/vsearch_transrate/good.unique_headers_adult.larva.centroid.trinity.fasta
2. kallisto index -i adult.larva.idx good.unique_headers_adult.larva.centroid.trinity.fasta
3. kallisto quant -i adult.larva.idx -o adult.larva.merged --plaintext adult.larva.1.corrected.fastq adult.larva.2.corrected.fastq 

##Blast kallisto results to uinprot database 
1. grep 20 best contigs based on tpm from good.unique_headers_adult.larva.centroid.trinity.fasta
2. grep -w to force it to only match whole word (it would pull 8576, 18576, 28576 etc)
3. nano adult.larvadb
4. blastx -db uniprot -query adult.larvadb -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 5 > adult_larva_txn_blast
5. cat adult_larva_txn_blast | awk '{print $1}' | uniq > unique

		9060
		560
		106883
		18760
		110916
		16335
		24983
		35148
6. Lots of hits, but only 8 unique contigs...take best hit for each contig based on %ID
7. All cellular process type of things

		Actin
		Cytochromes
		Elongation factors
		

##Panther
1. Take results of blast from kallisto and download onto my computer
2. Copy column 2 (upiprot headers)	
3. Paste into new column
4. Find sp| and replace with nothing
5. In the next column run =LEFT(F1,FIND("|",F1)-1)
6. Copy this column (only the uniprot ID to new file) paste special, values
7. Save as .csv	
8. Download the genelist file (downloaded to Lindsay directory)
9. See pie chart (nothing really interesting again)
10. Download piecharts
11. Do this with adult and larva too


##Kallisto on vsearch merged file (consensus sequence) with larva reads 
1. kallisto quant -i adult.larva.idx -o adult.larva.merged_larva --plaintext no.trimmed.larva.1.corrected.fastq no.trimmed.larva.2.corrected.fasta

##Kallisto on vsearch merged file (consensus sequence) with adult reads 
1. kallisto quant -i adult.larva.idx -o adult.larva.merged_adult --plaintext no.trimmed.adult.1.corrected.fastq no.trimmed.adult.2.corrected.fastq

##Blast w/ uniprot
**WD: /mnt/data3/lah/transcriptome_work/kallisto/blast**

1. Grab all of the top contig hits from vsearch file
2. Download files in to excel and grab top 20 from adult, larva, and top 10 combined


#####adult#####
1. grep -w -A1 -f adult.larva.merged_adult_top20 good.unique_headers_adult.larva.centroid.trinity.fasta > adult_top_20_contigs
2. 4. blastx -db uniprot -query adult_top_20_contigs -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 5 > adult.larva_adult

#####larva#####
1.  grep -w -A1 -f adult.larva.merged_larva_top20 good.unique_headers_adult.larva.centroid.trinity.fasta > larva_top_20_contigs
2. blastx -db uniprot -query larva_top_20_contigs -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 5 > adult.larva_larva

#####both#####
 
1. grep -w -A1 -f adult.larva.merged_adult.larva_top20 good.unique_headers_adult.larva.centroid.trinity.fasta > adult.larva_top_20_contigs

2. blastx -db uniprot -query adult.larva_top_20_contigs -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 5 > adult.larva_both

**Some of the contigs didn't hit to UniProt database**

##Counting # of transcripts 
1. In excel
2. =IF(D2=0,0,1)
3. Sum function
4. Larva has 85194 transcripts 
5. Adult has 94413 transcripts

#####Finding amount in common
1. In excel 
2. =(IF(AND(D2=1,F2=1),1,0))
3. Number in common 63950
4. Adult has 63950 unique
5. Larva has 21243 unique


##Mapping each tissue's reads back to vsearch, transrate assembly using bwa-mem
**WD:/mnt/data3/lah/transcriptome_work/bwa/adult**
**WD:/mnt/data3/lah/transcriptome_work/bwa/larva** 

1. ln -s /mnt/data3/lah/transcriptome_work/transrate/vsearch_transrate/good.unique_headers_adult.larva.centroid.trinity.fasta
2. ln -s individual corrected reads from: /mnt/data3/lah/transcriptome_work/kallisto/
3. bwa index good.unique_headers_adult.larva.centroid.trinity.fasta

**adult**

1. bwa mem -t 5 ../good.unique_headers_adult.larva.centroid.trinity.fasta no.trimmed.adult.1.corrected.fastq no.trimmed.adult.2.corrected.fastq > adult.sam

**larva**

1.bwa mem -t 5 ../good.unique_headers_adult.larva.centroid.trinity.fasta no.trimmed.larva.1.corrected.fastq no.trimmed.larva.2.corrected.fastq > larva.sam

#BUSCO on both Transrate and Vsearched merged assemblies
**WD:/mnt/data3/lah/busco**

####Vsearch####
1. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonoia.transcriptome.vsearch.eukaryota.busco -in good.unique_headers_adult.larva.centroid.trinity.fasta -l eukaryota/

		Total running time:   3259.058395385742 seconds
		Total complete BUSCOs found in assembly (<2 sigma) :  108       (233 duplicated).
		Total BUSCOs partially recovered (>2 sigma) :  17
		Total groups searched: 429
		Total BUSCOs not found:  71
		
		Summarized benchmarks in BUSCO notation:
		
		C:79%[D:54%],F:3.9%,M:16%,n:429

		Representing:
				341	Complete Single-Copy BUSCOs
				233	Complete Duplicated BUSCOs
				17	Fragmented BUSCOs
				71	Missing BUSCOs
				429	Total BUSCO groups searched

2. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonoia.transcriptome.vsearch.arthropoda.busco -in good.unique_headers_adult.larva.centroid.trinity.fasta -l arthropoda/

		Summarized benchmarks in BUSCO notation:
		C:81%[D:54%],F:11%,M:7.5%,n:2675

		Representing:
			2170	Complete Single-Copy BUSCOs
			1465	Complete Duplicated BUSCOs
			304	Fragmented BUSCOs
			201	Missing BUSCOs
			2675	Total BUSCO groups searched



####Transrate####
1. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonia.transcriptome.transrate.eukaryota.busco -in good.merge.fasta -l eukaryota/		
				
				Summarized benchmarks in BUSCO notation:
			C:79%[D:73%],F:3.9%,M:16%,n:429

			Representing:
				341	Complete Single-Copy BUSCOs
				314	Complete Duplicated BUSCOs
				17	Fragmented BUSCOs
				71	Missing BUSCOs
				429	Total BUSCO groups searched
				
 2. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonia.transcriptome.transrate.arthropoda.busco -in good.merge.fasta -l arthropoda/
 
 			
 		Summarized benchmarks in BUSCO notation:
			C:81%[D:74%],F:11%,M:7.2%,n:2675

		Representing:
			2182	Complete Single-Copy BUSCOs
			1991	Complete Duplicated BUSCOs
			300	Fragmented BUSCOs
			193	Missing BUSCOs
			2675	Total BUSCO groups searched		
