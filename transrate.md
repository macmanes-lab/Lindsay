#Transrate
http://hibberdlab.com/transrate/

- Transrate is software for deep inspection and quality analysis of de-novo transcriptome assemblies. It works by examining your assembly in detail, comparing it to experimental evidence such as the sequencing reads, and providing insight about its quality and usefulness in various situations. This can allow you to choose between assemblers and parameters, filter out the bad contigs from an assembly, and help decide when to stop trying to improve the assembly.


- If above .25, it's acceptable 
- synthetic runs (with no error) have about .60

##Adult##

WD: /mnt/data3/lah/transrate/adult/

*This transcriptome wasn't trimmed within bless

*There was no khmer normalization 

1. copy files to transrate/adult/ folder 
	A. Assembled transcriptome: adult.notrim.bless.nonorm.trinity.fasta
	B. left read: no.trimmed.adult.1.corrected.fastq
	C. right read: no.trimmed.adult.2.corrected.fastq 
	D. reference: tribolium.protein.fa

2. transrate -a adult.notrim.bless.nonorm.trinity.fasta -r tribolium.protein.fa -o adult.nontrim.ec.no.norm.transrate -l no.trimmed.adult.1.corrected.fastq -i no.trimmed.adult.2.corrected.fastq -t 10
3. Gives me lots of files. I want the good.adult.notrim.bless.nonorm.trinity.fasta

##Larva##

WD: /mnt/data3/lah/transrate/larva/
*This transcriptome wasn't trimmed within bless

*There was no khmer normalization 

1. copy files to transrate/larva/ folder 
	A. Assembled transcriptome: larva.notrim.bless.nonorm.trinity.fasta
	B. left read: no.trimmed.larva.1.corrected.fastq
	C. right read: no.trimmed.larva.2.corrected.fastq 
	D. reference: tribolium.protein.fa
	
2. tmux new -s transrate	

3. transrate -a larva.notrim.bless.nonorm.trinity.fasta -r tribolium.protein.fa -o larva.transrate -l no.trimmed.larva.1.corrected.fastq -i no.trimmed.larva.2.corrected.fastq -t 10