#!/usr/bin/python

"""
Date        : december 2016
Course      : Fundamentals of Fuzzy Logic, UvA
Project name: Fuzzy Bed and Breakfast
Students    : David Smelt, Alex Khawalid, Verna Dankers

Description : Writes n lines from input_csv_file to output_csv_file
Usage       : python input_csv_file n output_csv_file
"""


import argparse
import pandas

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@',
    )

    parser.add_argument(
        'inp',
        help="Csv file with input data",
    )

    parser.add_argument(
        'n',
        help="Number of lines",
        default='1000',
        type=int,
        nargs='?'
    )

    parser.add_argument(
        'outp',
        help="Name for csv file to write output to",
        default='setje.csv',
        nargs='?'
    )

    args = parser.parse_args()

    with open(args.inp,'r') as fin:
        pandas.options.mode.chained_assignment = None
        data = pandas.read_csv(fin,nrows=args.n)
        data = data.to_csv(args.outp)

