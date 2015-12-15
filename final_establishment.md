##Bless adult

	bless -read1 harmonia_adult.R1.fastq -read2 harmonia_adult.R2.fastq -prefix no.trimmed.adult -kmerlength 25

##Bless Larva

	bless -read1 harmonia_larva.R1.fastq -read2 harmonia_larva.R2.fastq -prefix no.trimmed.larva -kmerlength 25

##Trinity


	Trinity --seqType fq --max_memory 100G --trimmomatic --left adult.larva.1.corrected.fastq --right adult.larva.2.corrected.fastq --CPU 50 --output larva.adult.notrim.bless.nonorm.trinity --SS_lib_type RF --quality_trimming_params "ILLUMINACLIP:/opt/trinity/trinity-plugins/Trimmomatic-0.30/adapters/TruSeq3-PE.fa:2:40:15 LEADING:2 TRAILING:2 MINLEN:25" --full_cleanup
	
##Transrate


	transrate --assembly larva.adult.notrim.bless.nonorm.trinity.Trinity.fasta --left adult.larva.1.corrected.fastq --right adult.larva.2.corrected.fastq --threads 25	

##BUSCO
	python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o transrate.optimized.trinity.merged.arthropoda.busco -in good.larva.adult.notrim.bless.nonorm.trinity.Trinity.fasta -l arthropoda/ -c 25

##Salmon
*index*

	salmon index -t  good.larva.adult.notrim.bless.nonorm.trinity.Trinity
*quant*

	salmon quant -p 32 -i salmon.trinity.merged -l MSR -1 adult.larva.1.corrected.fastq -2 adult.larva.2.corrected.fastq -o salmon_trinity_merged	
##Kallisto
*index*

	kallisto index -i trinity.merged good.larva.adult.notrim.bless.nonorm.trinity.Trinity.fasta 

*quant*

	kallisto quant -i trinity.merged -o trinity.merged.kallisto --plaintext adult.larva.1.corrected.fastq adult.larva.2.corrected.fastq

##Sort

*salmon*

	awk '1>$3{next}1' salmon_trinity_merged/quant.sf | awk '{print $1}' | sed  '1d' > salmon.trinity.merged.list

*kallisto*
	
	awk '1>$5{next}1' trinity.merged.kallisto/abundance.tsv | awk '{print $1}' | sed  '1d' > kallisto.trinity.merged.list

*combine*

	cat *list | sort | uniq > highexp.list

*split*


	split -l 12000 highexp.list
*grab*
	
	for i in `cat xaa`; do grep --no-group-separator --max-count=1 -A1 -w $i ../good.larva.adult.notrim.bless.nonorm.trinity.Trinity.fasta >> xah.fa; done &	...

*combine*	

	cat *.fa >> combined.fa
	
##Transrate 


	transrate --assembly combined.fa --left ../adult.larva.1.corrected.fastq --right ../adult.larva.2.corrected.fastq --threads 25		

##BUSCO 
	python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o trinity.merged.tpm_greater_than_.5.arthropoda.busco -in good.combined.fa -l arthropoda/ -c 25