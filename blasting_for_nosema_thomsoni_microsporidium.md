#blasting for nosema thomsoni-like microsporidium
	
###does this parasite promote color change in *Hamonia axyridis*?
WD: /mnt/data3/lah/blast/nosema_blast

1. make database of abyss reads
	
		From optimization experiments using the bless trimmed, khmer normalized abyss run K111
			/mnt/data3/lah/abyss/trimmed.norm.bless.error.corrected.OPTIMAL/k111/k111-scaffolds.fa
			
		makeblastdb -in k111-scaffolds.fa -out harmonia_optimize_genome -dbtype nucl	
2. Find 16s sequences from nosema thomsoni 
3. nano nosema_thomsoni
4. 