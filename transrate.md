#Transrate
http://hibberdlab.com/transrate/

- Transrate is software for deep inspection and quality analysis of de-novo transcriptome assemblies. It works by examining your assembly in detail, comparing it to experimental evidence such as the sequencing reads, and providing insight about its quality and usefulness in various situations. This can allow you to choose between assemblers and parameters, filter out the bad contigs from an assembly, and help decide when to stop trying to improve the assembly.


- If above .25, it's acceptable 
- synthetic runs (with no error) have about .60

##Adult##

WD: /mnt/data3/lah/transrate/

*This transcriptome wasn't trimmed within bless

*There was no khmer normalization 

1. copy files to transrate folder 
	A. Assembled transcriptome: adult.notrim.bless.nonorm.trinity.fasta
	B. left read: harmonia_adult.R1.fastq
	C. right read: harmonia_adult.R2.fastq  
	D. reference: tribolium.protein.fa

2. transrate -a adult.notrim.bless.nonorm.trinity.fasta -r tribolium.protein.fa -o adult.nontrim.ec.no.norm.transrate -l harmonia_adult.R1.fastq -i harmonia_adult.R2.fastq -t 10