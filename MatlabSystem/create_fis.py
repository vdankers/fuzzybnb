#!/usr/bin/python2

"""
Date         : december 2016
Course       : Fundamentals of Fuzzy Logic, University of Amsterdam
Project name : Fuzzy Bed and Breakfast
Authors      : David Smelt, Alex Khawalid, Verna Dankers

Description  : Output a Matlab FIS based on training data
Cmdline args : training_features training_prices number_mfs_input
               number_mfs_output inference_system
Example usage: python2 ./create_fis.py train_features.csv train_prices.csv 5 20
               mamdani

"""

import argparse
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas

def display_clusters(data, columns, nclusters):
    """
    Create subplots of all features with their
    distribution of data points and clusters
    as determined by the KMeans algorithm.
    """

    labels = dict()
    rule_data = dict()
    for i, column in enumerate(columns):
        xpts = np.array(data[column])

        km = KMeans(n_clusters=nclusters)
        km.fit(xpts.reshape(-1,1))

        cntr = km.cluster_centers_
        kmlabels = km.labels_

        rule_data[column] = get_rule_data(cntr, kmlabels)

        labels[column] = (xpts, kmlabels, list(cntr.flatten()))

    return (rule_data, labels)

def find_min_max(columns, all_labels):
    """
    For every cluster of every feature, find the
    minimum and maximum value of the cluster.
    """
    all_parameters = dict()
    for column in columns:
        xpts, labels, cntr = all_labels[column]
        parameters = dict()
        for label in set(labels):
            center = round(cntr[label],1)
            parameters[center] = dict()
            parameters[center]['max'] = 0
            parameters[center]['min'] = 1000000

        for i, label in enumerate(labels):
            center = round(cntr[label],1)
            if xpts[i] < parameters[center]['min']:
                parameters[center]['min'] = xpts[i]
            if xpts[i] > parameters[center]['max']:
                parameters[center]['max'] = xpts[i]
        all_parameters[column] = parameters
    return all_parameters

def set_parameters(min_max, sugeno=0):
    """
    Set the parameters for the membership functions
    of all features.
    """
    parameters = {column : dict() for column in min_max.keys()}
    mfstext = {column : dict() for column in min_max.keys()}
    max_values = {column : dict() for column in min_max.keys()}
    for column in min_max:
        sorted_clusters = sorted(min_max[column].keys())

        # Create fuzzy memberships by +10% or -10%
        rng = (sorted_clusters[-1] - sorted_clusters[0]) / 10
        max_value = 0
        for cluster in sorted_clusters:
            mf = ''
            # leftmost membership function - trapezoidal
            if cluster == sorted_clusters[0]:
                a = 0
                c = round(min_max[column][cluster]['max'] + rng,1)
                mf = 'trapmf'
                cluster_params = [a,a,cluster,c]
            # rightmost membership function - trapezoidal
            elif cluster == sorted_clusters[-1]:
                a = round(min_max[column][cluster]['min'] - rng,1)
                c = round(min_max[column][cluster]['max'],1)
                mf = 'trapmf'
                cluster_params = [a,cluster,c,c]
                if c > max_value:
                    max_value = c
            # triangular membership function
            else:
                a = round(min_max[column][cluster]['min'] - rng,1)
                c = round(min_max[column][cluster]['max'] + rng,1)
                mf = 'trimf'
                cluster_params = [a,cluster,c]
            b = cluster
            parameters[column][cluster] = (a,b,c)
            if sugeno:
                mfstext[column][cluster] = ":'constant'," + str([cluster])
            else:
                mfstext[column][cluster] = ":'"+mf+"'," + str(cluster_params).replace(',','')
        max_values[column] = max_value
    return (parameters, mfstext, max_values)

def plot_mf(data, parameters, n, m):
    """
    Draw subplots containing the data distribution
    and the membership functions as determined
    by the application of clustering.
    """
    for i, column in enumerate(parameters):
        xpts = np.array(data[column])
        plt.subplot(n,m,i+1)
        plt.scatter(xpts,len(xpts) *[0.1], alpha=0.01)
        plt.axis([min(xpts),max(xpts),0,1])
        sorted_clusters = sorted(parameters[column].keys())

        for cluster in sorted_clusters:
            a,b,c = parameters[column][cluster]
            if cluster == sorted_clusters[0]:
                plt.plot([a, b], [1,1], 'k-')
                plt.plot([b, c], [1,0], 'k-')
            elif cluster == sorted_clusters[-1]:
                plt.plot([a, b], [0,1], 'k-')
                plt.plot([b, c], [1,1], 'k-')
            else:
                plt.plot([a, b], [0,1], 'k-')
                plt.plot([b, c], [1,0], 'k-')

        plt.yticks([0,1])
        plt.xlabel('$'+column.replace('_','\_')+'$',fontsize=14)


def get_rule_data(cntr, labels):
    """
    Return for each cluster label the number of the cluster
    when the clusters are ordered from left to right.
    """
    cntr = list(cntr.flatten())

    sorted_cntr = sorted(cntr)
    cntr_to_index = dict()
    for i, entry in enumerate(sorted_cntr):
        cntr_to_index[entry] = i + 1

    cntr = [cntr_to_index[center] for center in cntr]
    return [cntr[label] for label in labels]


def create_rulebase(data, rule_data_features, rule_data_price, columns):
    """
    Create rules from the clusters of accommodations' features
    and price.
    """
    rules = []
    for i in range(len(data)):
        rule = ""
        for j, column in enumerate(columns):
            if j > 0:
                rule += " "
            if j < 10:
                labels = rule_data_features
            label = labels[column][i]
            if (column == 'review_scores_location' or column == 'review_scores_value') and label == 10:
                label = 9
            rule += "%d" % (label)
        rule += ", %d (1) : 1" % (rule_data_price['price'][i])
        rules.append(rule)
    return rules

def add_membershipfunctions(fis, columns, nclusters, paramstext, max_values, name):
    """
    Add the text for the membership functions
    to the text of a Matlab FIS.
    """
    for i, column in enumerate(columns):
        fis += "[%s%d]\n" % (name, i+1)
        fis += "Name='%s'\n" % (column)
        fis += "Range=[0 %d]\n" % (max_values[column])
        fis += "NumMFs=%d\n" % (nclusters)
        for i, key in enumerate(sorted(paramstext[column])):
            fis += "MF%d='mf%d'%s\n" % (i+1,i+1, paramstext[column][key])
        fis+="\n"
    return fis

def create_fis(training_features, training_prices, clusters_features, clusters_price, system):
    """
    Creates a Matlab FIS based on training data in CSV format,
    a type of inference system and numbers of membership functions
    for input variables and the output variable.
    """
    data = pandas.read_csv(training_features)
    columns = data.columns
    rule_data_features, labels_features = display_clusters(data,columns,
        clusters_features)
    min_max = find_min_max(columns, labels_features)
    params, paramstext, max_values = set_parameters(min_max)

    data_price = pandas.read_csv(training_prices)
    rule_data_price, labels_price = display_clusters(data_price,["price"],
        clusters_price)
    min_max_price = find_min_max(["price"], labels_price)
    params_price, price_text, max_values_price = set_parameters(min_max_price,0)

    rules = list(set(create_rulebase(data, rule_data_features, rule_data_price,
        columns)))

    if system == 'sugeno':
        system_name = 'airbnb_sugeno_auto'
        fis = "[System]\nName='%s'\nType='sugeno'\nVersion=2.0\n" % (system_name)
        fis += "NumInputs=%d\nNumOutputs=1\nNumRules=%d" % (len(columns), len(rules))
        fis += "\nAndMethod='prod'\nOrMethod='probor'\nImpMethod='prod'"
        fis += "\nAggMethod='sum'\nDefuzzMethod='wtaver'\n\n"
    else:
        system_name = 'airbnb_mamdani_auto'
        fis = "[System]\nName='%s'\nType='mamdani'\n" % (system_name)
        fis += "Version=2.0\nNumInputs=%d\nNumOutputs=1" % (len(columns))
        fis += "\nNumRules=%d\nAndMethod='prod'\nOrMethod='max'\n" % (len(rules))
        fis += "ImpMethod='prod'\nAggMethod='max'\nDefuzzMethod='centroid'\n\n"

    fis = add_membershipfunctions(fis, columns, clusters_features, paramstext,
        max_values, "Input")
    fis = add_membershipfunctions(fis, ['price'], clusters_price, price_text,
        max_values_price, "Output")
    fis += "[Rules]\n"
    fis += ("\n").join(list(set(rules)))
    with open(system_name + ".fis",'w') as f:
        f.write(fis)

if __name__ == '__main__':

    # Define command line arguments
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@',
    )
    parser.add_argument(
        'train_x',
        help='CSV file with features of accommodations',
        default='train_features.csv'
    )
    parser.add_argument(
        'train_y',
        help='CSV file with prices of accommodations',
        default='train_prices.csv'
    )
    parser.add_argument(
        'mf_input',
        help='Number of membership functions for input variables',
        default=5,
        type=int
    )
    parser.add_argument(
        'mf_output',
        help='Number of membership functions for output variable',
        default=20,
        type=int
    )
    parser.add_argument(
        'system',
        help='Type of inference system',
        default='mamdani'
    )

    args = parser.parse_args()

    create_fis(args.train_x, args.train_y, args.mf_input, args.mf_output,
        args.system)
