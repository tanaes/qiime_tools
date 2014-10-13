#!/usr/bin/env python

import argparse
import os

from qiime.golay import encode
from cogent.parse.fastq import MinimalFastqParser

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input_dir", type=str, default="./", help="directory of input fastqs")
parser.add_argument("-o","--output_dir", type=str, default="./", help="directory to output files")
parser.add_argument("-l","--linker", type=str, default="YATGCTGCCTCCCGTAGGAGT", help="linker primer sequence [default = YATGCTGCCTCCCGTAGGAGT]")

getBin = lambda x, n: str(bin(x))[2:].zfill(12)

def main():

    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    linker = args.linker

    i = 0

    output_fastq_fp = os.path.join(output_dir,'demultiplexed.fastq')
    output_fastq = open(output_fastq_fp, 'w')
    output_map_fp = os.path.join(output_dir,'demultiplexed_map.txt')
    output_map = open(output_map_fp, 'w')
    output_map.write("#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tReads\tDescription\n")



    for fastq in os.listdir(input_dir):
        if fastq.endswith('.fastq'):
            try:
                fastq_file = open(os.path.join(input_dir,fastq),'Ur')
            except IOError:
                print "Could not open file ", fastq
                continue

            i += 1

            barcode_seq = encode([int(x) for x in list(str(bin(i))[2:].zfill(12))])

            barcode_qual = "I"*12

            reads = 0
            for header, seq, qual in MinimalFastqParser(fastq_file):
                reads += 1
                output_fastq.write("@%s\n" % header)
                output_fastq.write("{0}{1}\n".format(barcode_seq,seq))
                output_fastq.write("+%s\n" % header)
                output_fastq.write("{0}{1}\n".format(barcode_qual,qual))

            output_map.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(fastq,barcode_seq,linker,reads,fastq))

    output_map.close()
    output_fastq.close()

if __name__ == "__main__":
    main()




