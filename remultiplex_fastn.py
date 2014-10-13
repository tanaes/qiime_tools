#!/usr/bin/env python

import argparse
import os

from qiime.golay import encode
from cogent.parse.fastq import MinimalFastqParser
from cogent.parse.fasta import MinimalFastaParser

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='This script takes a folder of separate fasta/q files and remultiplexes them, adding fake golay12 barcodes and linker primers on to the front. Will try to combine all files in the input directory that end with the file extension specified by the -t/--type option.')
parser.add_argument("-i","--input_dir", type=str, default="./", help="directory of input fastqs/fastas")
parser.add_argument("-o","--output_dir", type=str, default="./", help="directory to output files")
parser.add_argument("-l","--linker", type=str, default="YATGCTGCCTCCCGTAGGAGT", help="linker primer sequence [default = YATGCTGCCTCCCGTAGGAGT]")
parser.add_argument("-t","--type", type=str, default="fasta", help="file type (fasta or fastq; default = fasta)")

getBin = lambda x, n: str(bin(x))[2:].zfill(12)

def main():

    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    linker = args.linker
    filetype = args.type

    i = 0

    output_fastx_fp = os.path.join(output_dir,'remultiplexed.' + filetype)
    output_fastx = open(output_fastx_fp, 'w')
    output_map_fp = os.path.join(output_dir,'remultiplexed_map.' + filetype + '.txt')
    output_map = open(output_map_fp, 'w')
    output_map.write("#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tReads\tDescription\n")



    for fastx in os.listdir(input_dir):
        if fastx.endswith(filetype):
            try:
                fastx_file = open(os.path.join(input_dir,fastx),'Ur')
            except IOError:
                print "Could not open file ", fastx
                continue

            i += 1

            barcode_seq = encode([int(x) for x in list(str(bin(i))[2:].zfill(12))])

            barcode_qual = "I"*12

            reads = 0
            if filetype in ('fastq','fq','fsq','fnq'):
                for header, seq, qual in MinimalFastqParser(fastx_file):
                    reads += 1
                    output_fastx.write("@%s\n" % header)
                    output_fastx.write("{0}{1}\n".format(barcode_seq,seq))
                    output_fastx.write("+%s\n" % header)
                    output_fastx.write("{0}{1}\n".format(barcode_qual,qual))
            elif filetype in ('fasta','fa','fsa','fna'):
                for header, seq in MinimalFastaParser(fastx_file):
                    reads += 1
                    output_fastx.write(">%s\n" % header)
                    output_fastx.write("{0}{1}\n".format(barcode_seq,seq))

            output_map.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(fastx,barcode_seq,linker,reads,fastx))

    output_map.close()
    output_fastx.close()

if __name__ == "__main__":
    main()




