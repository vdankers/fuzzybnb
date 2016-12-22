#!/usr/bin/python

"""
Date        : December 22, 2016
Course      : Fundamentals of Fuzzy Logic, University of Amsterdam
Project name: Fuzzy Bed and Breakfast
Authors     : David Smelt, Alex Khawalid, Verna Dankers

Description : Writes either n random lines or, with argument --norandom, the
              first n lines from input_csv_file to output_csv_file.
Usage       : python input_csv_file n output_csv_file --norandom
"""


import argparse
import pandas
import numpy.random


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
    parser.add_argument(
        '--norandom',
        help='Disable random shuffling of input rows',
        action='store_true'
    )

    data = None
    pandas.options.mode.chained_assignment = None
    args = parser.parse_args()

    if args.norandom:
        data = pandas.read_csv(args.inp, nrows=args.n)
    else:
        # Reading the entire CSV file with Pandas is the most reliable method
        # to get the total number of rows
        numpy.random.seed(0)
        data = pandas.read_csv(args.inp)
        data = data.reindex(numpy.random.permutation(data.index))
        data = data.head(n=args.n)

    data.to_csv(args.outp)
