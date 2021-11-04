#!/bin/bash
#SBATCH --partition=bgmp        ### Partition
#SBATCH --job-name=dedup     ### Job Name
#SBATCH --output=dedup_%j.out         ### File in which to store job output
#SBATCH --error=dedup_%j.err          ### File in which to store job error messages
#SBATCH --time=1-00:00:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1               ### Number of nodes needed for the job
#SBATCH --cpus-per-task=1
#SBATCH --account=bgmp      ### Account used for job submission
#SBATCH --mail-user='jlee26@uoregon.edu'
#SBATCH --mail-type=END,FAIL
conda activate bgmp_py39

# #sort .sam file:
# samtools sort /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam -o /projects/bgmp/jlee26/bioinformatics/Bi624/Deduper-jlee26/Part3/sorted_C1_SE_uniqAlign.sam

# official
./lee_deduper.py -u /projects/bgmp/jlee26/bioinformatics/Bi624/Deduper-jlee26/STL96.txt -f /projects/bgmp/jlee26/bioinformatics/Bi624/Deduper-jlee26/Part3/sorted_C1_SE_uniqAlign.sam

# # test
# ./lee_deduper.py -u /projects/bgmp/jlee26/bioinformatics/Bi624/Deduper-jlee26/STL96.txt -f /projects/bgmp/jlee26/bioinformatics/Bi624/Deduper-jlee26/Part1/sort.sam
