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
		
###transcriptome file was empty

		figured this out bc used abyss-fac on it
		
####transcriptome 
**OWD: /mnt/data3/lah/transcriptome_work/vsearch**

#Blat
blat -noHead k121-scaffolds.fa adult.larva.centroid.trinity.fasta harmonia.psl

		Loaded 831343170 letters in 515159 sequences
		Searched 105315076 bases in 130500 sequences

#L_RNA_scaffolder.sh
L_RNA_scaffolder.sh -d /share/L_RNA_scaffolder -i harmonia.psl -j k121-scaffolds.fa

	abyss-fac L_RNA_scaffolder.fasta 
	N50= 4163

	abyss-fac k121-scaffolds.fa
	N50= 4109
	
	abyss-fac -e 830000000 L_RNA_scaffolder.fasta
	NG50 = 3908
#bwa
1. bwa index -p harmonia ../L_RNA_scaffolder.fasta

		seqtk mergepe \
		/mnt/data3/lah/adult_transcriptomes/rcorrector/30129/30129_TAGCTT_BC6PR5ANXX_L008_001.R1.cor.fq \
		/mnt/data3/lah/adult_transcriptomes/rcorrector/30129/30129_TAGCTT_BC6PR5ANXX_L008_001.R1.cor.fq \
		| skewer -Q 2 -t 10 -x /share/trinityrnaseq/trinity-plugins/Trimmomatic/adapters/TruSeq3-PE-2.fa - -1 \
		| extract-paired-reads.py -p - -s /dev/null - \
		| bwa mem -p -t 10 harmonia - \
		| samtools view -T . -bu - \
		| samtools sort -l 0 -O bam -T tmp -@ 15 -m 22G -o 30129.harmonia.bam -
		
#merge 
samtools merge all.bam *.bam	
samtools index all.bam

#BESST_RNA
1. python /share/BESST_RNA/src/Main.py 1 -c ../L_RNA_scaffolder.fasta -f all.bam -e 3 -T 50000 -k 500 -d 1 -z 1000 -o scaffold_2_harmonia/

		abyss-fac -e 830000000 Scaffolds-pass1.fa
		NG50 4040
