#!/usr/bin/python

"""
Date        : December 9, 2016
Course      : Fundamentals of Fuzzy Logic, University of Amsterdam
Project name: Fuzzy Bed and Breakfast
Authors     : David Smelt, Alex Khawalid, Verna Dankers

Description : Plot membership functions for the data based on
              clusters as found by the KMeans algorithm
Usage       : Deprecated
"""

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas


def display_clusters(data, columns, nclusters, a, b):
    """
    Create subplots of all features with their
    distribution of data points and clusters
    as determined by the KMeans algorithm.
    """
    #plt.figure(figsize=(10, 1))
    labels = dict()
    rule_data = dict()
    for i, column in enumerate(columns):
        xpts = np.array(data[column])

        km = KMeans(n_clusters=nclusters)
        km.fit(xpts.reshape(-1,1))

        cntr = km.cluster_centers_

#         plt.subplot(a,b,i+1)
#         plt.scatter(xpts,len(xpts) *[0], alpha=0.01)

#         for pt in cntr:
#             plt.plot(pt[0], 0, 'rs')

#         plt.yticks([])
#         plt.axis([min(xpts),max(xpts),-1,1])
#         plt.xlabel('$'+column.replace('_','\_')+'$')
        kmlabels = km.labels_

        rule_data[column] = get_rule_data(cntr, kmlabels)

        labels[column] = (xpts, kmlabels, list(cntr.flatten()))
    #plt.show()
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
            center = cntr[label]
            parameters[center] = dict()
            parameters[center]['max'] = 0
            parameters[center]['min'] = 1000000

        for i, label in enumerate(labels):
            center = cntr[label]
            if xpts[i] < parameters[center]['min']:
                parameters[center]['min'] = xpts[i]
            if xpts[i] > parameters[center]['max']:
                parameters[center]['max'] = xpts[i]
        all_parameters[column] = parameters
    return all_parameters

def set_parameters(min_max):
    """
    Set the parameters for the membership functions
    of all features.
    """
    parameters = {column : dict() for column in min_max.keys()}
    for column in min_max:
        sorted_clusters = sorted(min_max[column].keys())
        rng = (sorted_clusters[-1] - sorted_clusters[0]) / 10
        for cluster in sorted_clusters:
            if cluster == sorted_clusters[0]:
                a = 0
                c = min_max[column][cluster]['max'] + rng
            elif cluster == sorted_clusters[-1]:
                a = min_max[column][cluster]['min'] - rng
                c = min_max[column][cluster]['max']
            else:
                a = min_max[column][cluster]['min'] - rng
                c = min_max[column][cluster]['max'] + rng
            b = cluster
            parameters[column][cluster] = (a,b,c)
    return parameters

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
        plt.xlabel('$'+column.replace('_','\_')+'$')

def get_rule_data(cntr, labels):
    cntr = list(cntr.flatten())

    sorted_cntr = sorted(cntr)
    cntr_to_index = dict()
    for i, entry in enumerate(sorted_cntr):
        cntr_to_index[entry] = i + 1

    cntr = [cntr_to_index[center] for center in cntr]
    return [cntr[label] for label in labels]


def create_rulebase(data, rule_data1, rule_data2, rule_data3, columns):
    rules = []
    for i in range(len(data)):
        rule = ""
        for j, column in enumerate(columns):
            if j > 0:
                rule += " AND "
            if j < 18:
                labels = rule_data1
            else:
                labels = rule_data2
            label = labels[column][i]
            rule += "IF %s is MF%d" % (column,label)
        rule += " THEN price is MF%d" % (rule_data3['price'][i])
        rules.append(rule)
    return rules

data1 = pandas.read_csv('result.csv')
columns1 = data1.columns
rule_data1, labels1 = display_clusters(data1,columns1[0:18],5,6,3)
rule_data2, labels2 = display_clusters(data1,columns1[18:33],5,6,3)
min_max1 = find_min_max(columns1[0:18], labels1)
min_max2 = find_min_max(columns1[18:33], labels2)
params1 = set_parameters(min_max1)
params2 = set_parameters(min_max2)
# plot_mf(data1, params1,6,3)
# plot_mf(data1, params2,6,3)

data2 = pandas.read_csv('prices.csv')
columns2 = data2.columns
rule_data3, labels3 = display_clusters(data2,columns2,5,1,1)
min_max3 = find_min_max(columns2, labels3)
params3 = set_parameters(min_max3)

# experiment fase
#rules = create_rulebase(data1, rule_data1, rule_data2, rule_data3, columns1)
