#!/usr/bin/env python
import argparse
import re
import sys

def get_args():
    parser = argparse.ArgumentParser(description="Files")
    parser.add_argument("-f", "--file", help="Specify the absolute pathway of the sorted .sam file.", required=True)
    parser.add_argument("-u", "--umi", help="Specify the absolute pathway to a text file with all the UMIs. Currently, this option is required.", required=True)
    parser.add_argument("-p", "--paired", help="Specify if reads are paired-end (y). Default is single-end.")
    
    return parser.parse_args()
args = get_args()

if args.paired == "y":
    print("Currently does not support paired-end reads. Please use single-end reads only. Exit script.")
    sys.exit()

# -u /projects/bgmp/jlee26/bioinformatics/Bi624/Deduper-jlee26/STL96.txt
# #sort test file:
# -f /projects/bgmp/jlee26/bioinformatics/Bi624/Deduper-jlee26/Part1/sort.sam
# #sort file:
# -f /projects/bgmp/jlee26/bioinformatics/Bi624/Deduper-jlee26/Part3/sorted_C1_SE_uniqAlign.sam

# read in umi file to create dictoinary of umis
if args.umi is not None:
    dict_umi = {} # key:umi; value:1
    with open(args.umi, "r") as f:
        while True:
            for line in f:
                line = line.strip()
                dict_umi[line] = 1
            break
# print(dict_umi)
# success!

def strand_specificity(samline):
    '''
    This function takes in a line in a sam file. This function returns a positive or negative string indicating a positive or reverse strand by looking at the decimal number for the 16 bit flag.
    '''
    decimal = int(samline[1])
    if ((decimal & 16) == 16): #checks bit 16
        rev_comp = True #if True (1), reverse complimented
        return "-"
    else:
        return "+"
# success!

def position(strandedness, cigarstring, tabline):
    '''
    This function takes in 3 arguments in the following order: the strandedness as '+' or '-', cigar string, and the left most mapping position. This returns the actual start position by accounting for the soft clippings and reverse and forward stranded reads.
    '''
    pos = int(tabline[3]) #left most mapping position
    if strandedness == "+": #forward read
        letters = re.findall('[A-Z]', cigarstring) #lists the letters of the cigar string
        if letters[0] == "S": #first soft-clipping occurance
            location = cigarstring.find('S') #location of the first soft-clipping occurance
            softclip = int(cigarstring[:location]) #finds amount of bases that was soft-clipped
            pos = pos - softclip #finds the adjusted left-most mapping position (accounting for soft-clip)
            return pos
        else: #doesn't have soft-clipping
            return pos
    else: #reverse strand
        letters = re.findall('[A-Z]', cigarstring) #lists the letters of the cigar string
        if letters[0] == "S": #first soft-clipping occurance 
            first_soft = cigarstring.find("S") #location of the soft-clipping occurance
            cigarstring = cigarstring[first_soft+1:] #removes soft-clipping since we don't care for reverse strand
        
        number = "" #initialize
        for char in cigarstring: #look at each character of the cigar string
            if char.isdigit():
                number += char #add the string of digits that's a digit
            else: #not a digit
                if char == "D" or char == "M" or char== "N" or char == "S":
                    number = int(number)
                    pos = pos + int(number) #adjusted start position (accounting for Deletion, M, N, and soft-clipping at the end)
                    number = "" #re-initialize
                elif char == "I":
                    number = "" #ignore insertion, since genome alignment doesn't exist
                    continue
                else:
                    print("ERROR! CIGAR string contains " + char + " at line " + tabline + ". This has not been accounted for in repositioning the start position.")
                    continue
        return pos
# success!


# read the .sam sorted file:
file_sam = open(args.file, "r")

# output written .sam file
file_output = open("/projects/bgmp/jlee26/bioinformatics/Bi624/Deduper-jlee26/Part3/output_deduped.sam", "w")
#file_output = open("/projects/bgmp/jlee26/bioinformatics/Bi624/Deduper-jlee26/Part3/output.sam", "w")

# initialize dictionary that'll keep tracking PCR duplicates
dict_info= {} # key: chrom#,startposition,strandedness,umi; value:.sam line currently reading
# initialize dictionary that'll reset dict_info for every new chromosome
dict_chrom_tracker = {} # key: chrom; value: 1

# report these values for the assignment
count_uniq_reads = 0
count_wrong_umis = 0
count_dup_removed = 0
dict_reads_per_chrom = {}

while True:
    line = file_sam.readline() #reading the line
    if line == "": #ends the while loop if the line doesn't contain any strings
        break
    else: #reading in the line
        line_original = line #keeps original line
        line = line.strip() #get rid of newline
        if line[0] == "@": #header lines
            file_output.write(line + "\n")
        else: #skip all the lines that starts with @, the header
            line = line.split() #tab-separate line
            umi = line[0][-8:] #last 8 characters of the QNAME col = UMIs
            if umi in dict_umi.keys(): #umi is one of the known UMI
                #print(umi, "yes")
                chrom = line[2] #chromosome number (RNAME)
                if chrom in dict_chrom_tracker.keys(): #checks to see if we're looking at the same chromosome
                    strand = strand_specificity(line) #strandedness, + or -
                    cigar = line[5] #cigar string
                    pos = position(strand, cigar, line) #finds adjusted start position
                    #print(umi, chrom, strand, cigar, line[3], pos)
                    
                    if (umi, chrom, strand, pos) not in dict_info.keys(): #indicates not a PCR duplicate
                        dict_info[umi,chrom,strand,pos] = line_original #add to dict_info
                        count_uniq_reads += 1 #counter
                        
                    else: #indicates a PCR duplicate
                        count_dup_removed += 1 #counter
                else: #looking at different chromosome
                    dict_chrom_tracker[chrom] = 1 #add the new chromosome into dict_tracker
                    for key, value in dict_info.items(): #add unique reads to the output .sam file
                        file_output.write(value)

                    dict_info = {} #re-initialize dict_info
                    strand = strand_specificity(line) #strandedness, + or -
                    cigar = line[5] #cigar string
                    pos = position(strand, cigar, line) #adjusted start position
                    #print(umi, chrom, strand, cigar, line[3], pos)
                    
                    if (umi, chrom, strand, pos) not in dict_info.keys(): #not a PCR duplicate. There should be nothing in dict_info
                        dict_info[umi,chrom,strand,pos] = line_original #add to dict_info
                        count_uniq_reads += 1 #counter
            else: #UMI doesn't exist
                count_wrong_umis += 1 #counter
                continue
            dict_reads_per_chrom[chrom] = len(dict_info) #find number of uniq reads for each chromosome
#print(len(dict_info))

for key, value in dict_info.items(): #add unique reads to the output .sam file
    file_output.write(value)
                
print("Uniq reads: ", count_uniq_reads, "\n", "Wrong UMIs: ", count_wrong_umis, "\n", "Dups removed: ", count_dup_removed)
#print(dict_chrom_tracker)
print("Number of unique reads for each chromosome: ", "\n", dict_reads_per_chrom)
#print(len(dict_info))

file_sam.close()
file_output.close()
