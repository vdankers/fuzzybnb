#!/usr/bin/python

"""
Date        : december 2016
Course      : Fundamentals of Fuzzy Logic, UvA
Project name: Fuzzy Bed and Breakfast
Students    : David Smelt, Alex Khawalid, Verna Dankers

Description : Convert membership functions to format readable by R or matlab
Usage       : python mfs.py
"""

import numpy as np
import re
import json

def build_R_memberships(fname):
    rows = [[], [], [], [], []]
    lines = []
    with open(fname) as f:
        for line in f.readlines():
            if line != "\n":
                line = re.sub("'(.+)': {|\(|},|}|\s", "",line)
                line = re.sub('(triangular:)', "[1,", line)
                line = re.sub('(trapezoidal:)', "[4,", line)
                line = "[" +re.sub('\)', "]", line) + "]"
                line = json.loads(line)

                lines.append(line)

                for term in line:
                    if len(term) < 5:
                        term.append(0)

                    i = 0
                    while (i < 5):
                        rows[i].append(term[i])
                        i+=1

    print 'Number of inputs: ' + str(len(lines)-1)
    return 'manualMFs <- matrix(c(' + str([val for sublist in rows for val in sublist]).strip('[]') + '), nrow=5, byrow=TRUE)'

def getvalues(fname):
    rows = {}
    lines = []
    with open(fname) as f:
        for line in f.readlines():
            if line != "\n":
                title = re.search("'(.+)'", line).groups()
                # print title[0]
                line = re.sub("'(.+)': {|\(|},|}|\s", "",line)
                line = re.sub('(triangular:)', "[1,", line)
                line = re.sub('(trapezoidal:)', "[4,", line)
                line = "[" +re.sub('\)', "]", line) + "]"
                line = json.loads(line)

                obj = {'name': title[0], 'vals': line}
                lines.append(obj)
    return lines

def build_ML_memberships(fname):
    fis = getvalues('membershipfunctions.txt')

    matlabstring = '''[System]
    Name='test'
    Type='sugeno'
    Version=2.0
    NumInputs=10
    NumOutputs=1
    NumRules=0
    AndMethod='prod'
    OrMethod='probor'
    ImpMethod='prod'
    AggMethod='sum'
    DefuzzMethod='wtaver'
    '''
    inps = 1
    for inp in fis:
        matlabstring += '\n[Input'+str(inps)+']\n'
        matlabstring += "Name='"+inp['name'] +"'\n"
        matlabstring += "Range=[0 1]\n"
        matlabstring += "NumMFs=" + str(len(inp['vals'])) + "\n"
        # print 'input ' + str(inps)
        i = 1
        for mfs_for_inp in inp['vals']:
            # print 'mf' + str(i)
            # print mfs_for_inp
            matlabstring += 'MF' + str(i) + "='mf" + str(i) + "':'"
            method = ''
            if mfs_for_inp[0] == 4:
                method = 'trapmf'
            if mfs_for_inp[0] == 1:
                method = 'trimf'

            matlabstring += method + "',["
            j = 1
            while j < len(mfs_for_inp):
                matlabstring += str(mfs_for_inp[j]) + ' '
                j += 1
            matlabstring += ']\n'
            i+=1
        inps +=1
    return matlabstring

# mfs = build_R_memberships('membershipfunctions.txt')
# mffile = open('./RLearn/mfs.R', 'w')
# mffile.write(mfs)
# mffile.close()

mfs = build_ML_memberships('membershipfunctions.txt')
print mfs
