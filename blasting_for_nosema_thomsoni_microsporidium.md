#blasting for nosema thomsoni-like microsporidium
	
###does this parasite promote color change in *Hamonia axyridis*?
WD: /mnt/data3/lah/blast/nosema_blast

1. make database of abyss reads
	
		From optimization experiments using the bless trimmed, khmer normalized abyss run K111
			/mnt/data3/lah/abyss/trimmed.norm.bless.error.corrected.OPTIMAL/k111/k111-scaffolds.fa
			
		makeblastdb -in k111-scaffolds.fa -out harmonia_optimize_genome -dbtype nucl	
2. Find 16s sequences from nosema thomsoni on genbank
3. nano nosema_thomsoni
4. tmux new -s blast
5. blastn -db harmonia_optimize_genome -query nosema_thomsoni -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > blast_for_microsporidium

		No hits!
		
6. tblastx -db harmonia_optimize_genome -query nosema_thomsoni -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > blast_for_microsporidium_2
		
		Top hit was for a plant fungal pathogen

7. Add more sequences from other noseam to nosema_thomsoni
8. nano nosema_thomsoni		
9. tmux at -t blast
10. blastn -db harmonia_optimize_genome -query nosema_thomsoni -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > blast_for_microsporidium_2

		No hits!
		
11. tblastx -db harmonia_optimize_genome -query nosema_thomsoni -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > blast_for_microsporidium_2

12. Grab top hits

		Grep -A10 contig k111-scaffolds.fa
		Top hit still verticillium dahliae and ladybug
13. Grab more sequences not just 16S...16s probably too specific
14. nano nosema_sp_not_16s
15. blastn -db harmonia_optimize_genome -query nosema_sp_not_16s -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > blast_for_microsporidium_3
		
		No hits 
16. make nosema sequences database?
17. makeblastdb -in nosema_sp_not_16s -dbtype nucl -out nosemadb
18. blastn -db nosemadb -query k111-scaffolds.fa -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > blast_for_microsporidium_4 

		No hits	and took a lot longer
		
19. tblastx -db harmonia_optimize_genome -query nosema_sp_not_16s -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > blast_for_microsporidium_5		
		
		Top hit had no hits in blast website
				

				

		