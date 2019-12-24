#!/bin/bash 
prefetch -O /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159 SRR976159
prefetch -O /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411 SRR978411
prefetch -O /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778 SRR971778
fasterq-dump -e 8 -f -t /home/usingh/work/urmi/hoap/test/athalData/sraData -O /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159 -o SRR976159.fastq /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159/SRR976159.sra
fasterq-dump -e 8 -f -t /home/usingh/work/urmi/hoap/test/athalData/sraData -O /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411 -o SRR978411.fastq /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411/SRR978411.sra
fasterq-dump -e 8 -f -t /home/usingh/work/urmi/hoap/test/athalData/sraData -O /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778 -o SRR971778.fastq /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778/SRR971778.sra
hisat2-build -p 8 -a -q /home/usingh/work/urmi/hoap/test/athalData/ref/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa /home/usingh/work/urmi/hoap/test/athalData/sraData/athalIndex/athalInd
hisat2 --dta-cufflinks -p 10 -x /home/usingh/work/urmi/hoap/test/athalData/sraData/athalIndex/athalInd -1 /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159/SRR976159_1.fastq -2 /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159/SRR976159_2.fastq -S /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159/SRR976159_hisat2.sam
hisat2 --dta-cufflinks -p 10 -x /home/usingh/work/urmi/hoap/test/athalData/sraData/athalIndex/athalInd -1 /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411/SRR978411_1.fastq -2 /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411/SRR978411_2.fastq -S /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411/SRR978411_hisat2.sam
hisat2 --dta-cufflinks -p 10 -x /home/usingh/work/urmi/hoap/test/athalData/sraData/athalIndex/athalInd -1 /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778/SRR971778_1.fastq -2 /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778/SRR971778_2.fastq -S /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778/SRR971778_hisat2.sam
samtools view -@ 8 -o /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159/SRR976159_hisat2.bam -b /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159/SRR976159_hisat2.sam
samtools sort -@ 8 -o /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159/SRR976159_hisat2_sorted.bam /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159/SRR976159_hisat2.bam
samtools view -@ 8 -o /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411/SRR978411_hisat2.bam -b /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411/SRR978411_hisat2.sam
samtools sort -@ 8 -o /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411/SRR978411_hisat2_sorted.bam /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411/SRR978411_hisat2.bam
samtools view -@ 8 -o /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778/SRR971778_hisat2.bam -b /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778/SRR971778_hisat2.sam
samtools sort -@ 8 -o /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778/SRR971778_hisat2_sorted.bam /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778/SRR971778_hisat2.bam
stringtie -G /home/usingh/work/urmi/hoap/test/athalData/ref/Arabidopsis_thaliana.TAIR10.45.gtf -o /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159/SRR976159_hisat2_sorted_stringtie.gtf /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR976159/SRR976159_hisat2_sorted.bam
stringtie -G /home/usingh/work/urmi/hoap/test/athalData/ref/Arabidopsis_thaliana.TAIR10.45.gtf -o /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411/SRR978411_hisat2_sorted_stringtie.gtf /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR978411/SRR978411_hisat2_sorted.bam
stringtie -G /home/usingh/work/urmi/hoap/test/athalData/ref/Arabidopsis_thaliana.TAIR10.45.gtf -o /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778/SRR971778_hisat2_sorted_stringtie.gtf /home/usingh/work/urmi/hoap/test/athalData/sraData/SRR971778/SRR971778_hisat2_sorted.bam