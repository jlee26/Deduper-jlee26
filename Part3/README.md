# Part 3 Deduper

## Code
### Script
./lee_deduper.py

### Description
input: sorted .sam file <br/>
output: PCR duplicate-free .sam file called output_deduped.sam

### Syntax
./lee_deduper.py -u <UMIs.file> -f <sorted_pcr_duplicate.sam>

## Assignment
File: ./dedup_16562176.out contains information of the output_deduped.sam file, including number of unique reads, number of wrong UMIs, number of reads removed due to duplication, and number of unique reads for each chromosome.<br/>
<br/>
.sam file was provided by our instructor, found on talapas:
- /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam <br/>
<br/>
This file was sorted and deduped using ./wrapper_deduper.sh <br/>
<br/>
The output_deduped.sam file is found on talapas:
- /projects/bgmp/jlee26/bioinformatics/Bi624/Deduper-jlee26/Part3/output_deduped.sam

