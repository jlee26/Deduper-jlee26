
# Deduper
## Part 1: Pseudocode
Juyoung Lee\
BI 624\
10/15/21

### Problem
PCR amplification is part of the Illumina sequencing process to sequence the reads. This step is important, as it helps create multiple fragments with adapters for sequencing, however, this step can create some strands to be overrepresented. These overrepresented strands, or PCR duplicates, can be sequenced, resulting in duplicate reads from the same cDNA. PCR duplicates can cause inaccurate downstream analysis, including RNA-seq, transcriptomics, differential expression, or genome assembly.

### Objective
Build a code to remove reference-based PCR duplicates. The data will be a single-end reads with 96 UMIs. The code will account for the same chromosome, start position, and strand specificity. It will also account for UMIs and soft clipping to remove any duplicates.

### Input and Output Files (Examples)
The deduper code will take a sorted .sam file using the following command:
``` samtools sort <file_name.sam> -o sort.sam ```
The deduper code will output a .sam file with a single copy of each read.\
\
Input: sort.sam\
Expected output: output.sam

### Developing an Algorithm (Pseudocode)
1. Use command line to sort by chromosome number (RNAME, SAM col 3), and pipeline to a new file.
2. In python, call the function (umi_organizer) and read in STL96.txt (creates a dictionary (dict_umi) with all UMIs)
3. Initialize dictionary (dict_info) to store chromosome, start position, and strand specificity. (Key: chrom,pos,strand,umi; value: .sam line currently reading)
4. Use python to open a new file and write to output.sam.
5. Use python to open and read the sorted .sam file (from #1).
6. Create a local variable (line) to store the line of the file, and skip the line that starts with "@" (if statement). Read line as tab separated.
7. Create a local variable (chrom) and store chromosome number (col 3).
8. Create an if statement (to check for start position):
    - If the *first letter* we see in the CIGAR (col 6) contains a letter 'S', create a variable (s) and store the number before the letter 'S' (use regex).
        - Create a new variable (pos) and store start position (col 4) - S
    - If no 'S' is present (at the first letter), create a variable (pos) and store start position (col 4).
9. Call a function (strand_specificity) and input the decimal number (col 2). (Returns a + or - in a variable (strand)).
10. Create a local variable (umi) and store the last 8 characters of QNAME (col 1).
11. Create an if statement (to append to the dictionary (dict_info)):
    - If chrom,pos,strand,umi does NOT exist in dict_info AND umi exists in dict_umi , then append to:
        - dict_info (Key: chrom,pos,strand,umi; Value: line)
    - If chrom,pos,strand,umi exists as Key in dict_info AND umi exists in dict_umi, then:
        - if umi != dict_info.key[last 8 characters], then append to:
            - dict_info (Key: chrom,pos,strand,umi; Value: line)
        - else, don't add to dictionary. #NOTE: this will only keep the first occurance of the read. For challenge, I could keep the read that has a higher quality?
12. Repeat for each row.
13. After running through the .sam file, write to new output.sam file by taking the values of dict_info using for loop.
14. Close all files.


### Functions
1. Function Header: def umi_organizer(tf):
    - Description: Takes in a text file with a list of 1 UMIs per row and returns a dictionary, dict_umi, with all the UMIs as values.
    - Input: test.txt\
        AAAAA\
        TTTTT\
        GGGGG\
        CCCCC
    - Output:\
        {0:'AAAAA',\
        1:'TTTTT',\
        2:'GGGGG',\
        3:'CCCCC'}
    - Pseudocode:
        1. Initalize dictionary (dict_umi).
        2. Read file.
        3. Create variable (line) and store in each line of the file.
        4. Append to dict_umi (key: 0:96; value: line)
        5. Return dict_umi
2. Function Header: def strand_specificity(num):
    - Description: Takes in a decimal number and determines if the bit 16 is True(1) or False(0). If True(1), sequence is reverse complemented, therefore returns a string "-". If False(0), sequence is not reverse complemented, thereefore returns a string "+". 
    - Input: 89
    - Output: "-"
    - Pseudocode:
        1. Takes in decimal number.
        2. If the binary number 16 is set to 1 (aka True), return variable (strand) as -
        3. Else: return variable (strand) as +
