#Optimize genome w/ transcriptome
####1. blat
####2. L_RNA scaffolder
		
		V1 genome
####3. BUSCO
_________________________________		
####1. Rcorrector
####2. Bwa to map corrected reads to v1 genome
####3. Samtools merge
####4. BESST.RNA

		V2 Genome	
####5. Busco			


#Blat
**WD:/mnt/data3/lah/better_genome**

#####Genome

Using trimmed,khmer normed, bless error corrected abyss file

**OWD: /mnt/data3/lah/abyss/trimmed.norm.bless.error.corrected.OPTIMAL/k121** 

#####Transcriptome
using vsearch merged, transrate improved transcriptome 
 **OWD:/mnt/data3/lah/transcriptome_work/transrate/vsearch_transrate**
good.unique_headers_adult.larva.centroid.trinity.fasta

	End of file reading 4 bytes
What I've tried:
		
		blat -noHead -t=dna /mnt/data3/lah/abyss/trimmed.norm.bless.error.corrected.OPTIMAL/k121/k121-scaffolds.fa -q=rna /mnt/data3/lah/transcriptome_work/transrate/vsearch_transrate/good.unique_headers_adult.larva.centroid.trinity.fasta output.psl
		
		blat -noHead -t=dna k121-scaffolds.fa -q=rna good.unique_headers_adult.larva.centroid.trinity.fasta output.psl
		
		blat -noHead -t=dna k121-scaffolds.fa -q=rna good.unique_headers_adult.larva.centroid.trinity.fasta harmonia.psl
		
		blat -t=dna k121-scaffolds.fa -q=rna good.unique_headers_adult.larva.centroid.trinity.fasta output.psl
		
		blat -noHead k121-scaffolds.fa good.unique_headers_adult.larva.centroid.trinity.fasta output.psl
		
		blat -noHead k121-scaffolds.fa good.unique_headers_adult.larva.centroid.trinity.fasta harmonia.psl	