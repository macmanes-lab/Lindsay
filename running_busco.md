##Running BUSCO

**WD: /mnt/data3/lah/busco**

1. Not in path... source ~/.profile

1. wget http://busco.ezlab.org/files/arthropoda_buscos.tar.gz
2. tar -zxvf arthropoda_buscos.tar.gz
3. ln -s /mnt/data3/lah/abyss/nontrimmed.bless.no.norm.no.txn/k111/k111-scaffolds.fa
4. tmux new -s busco
3. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonia.assembly.busco -in k111-scaffolds.fa -l arthropoda

		Summarized benchmarks in BUSCO notation:
			C:39%[D:23%],F:30%,M:30%,n:2675

		Representing:
			1050	Complete Single-Copy BUSCOs
			630	Complete Duplicated BUSCOs
			817	Fragmented BUSCOs
			808	Missing BUSCOs
			2675	Total BUSCO groups searched
7. mv run_harmonia.assembly.busco/ run_harmonia.assembly.arthropoda.busco
8. **Use eukaryote database so it's more comparable to cegma**
9. wget http://busco.ezlab.org/files/eukaryota_buscos.tar.gz
10. tar -zxvf eukaryota_buscos.tar.gz
11. tmux at -t busco
12. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonia.assembly.eukaryota.busco -in k111-scaffolds.fa -l eukaryota/		

		Summarized benchmarks in BUSCO notation:
		C:54%[D:32%],F:12%,M:33%,n:429

		Representing:
			235	Complete Single-Copy BUSCOs
			140	Complete Duplicated BUSCOs
			52	Fragmented BUSCOs
			142	Missing BUSCOs
			429	Total BUSCO groups searched
			
**Low when compared to cegma...try running it on nanopore data**

1. ln -s /mnt/data3/lah/nanopore/spades/harmonia.nanopore.spades/21.33.55.77.scaffolds.fasta
2. 	python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o nanopore.assembly.arthropoda -in 21.33.55.77.scaffolds.fasta -l arthropoda/		