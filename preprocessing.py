#!/usr/bin/python

"""
Date         : December 22, 2016
Course       : Fundamentals of Fuzzy Logic, University of Amsterdam
Project name : Fuzzy Bed and Breakfast
Authors      : David Smelt, Alex Khawalid, Verna Dankers

Description  : Preprocesses data
Cmdline args : input_csv fraction_train_set output_features.csv output_prices.csv
               --noverbose --norandom
Example usage: input_data.csv 0.8 --noverbose --norandom
               ... will hide verbose output
               ... will not randomize input data rows
               ... will output training(0.8) X -> train_features.csv
                               training(0.8) y -> train_prices.csv
                                   test(0.1) X -> test_features.csv
                                   test(0.1) y -> test_prices.csv
                                  cross(0.1) X -> cross_features.csv
                                  cross(0.1) y -> cross_prices.csv
"""

from __future__ import print_function
import argparse
import pandas as pd
import math
import csv
import numpy as np
from ast import literal_eval
from decimal import Decimal, ROUND_HALF_UP
from sklearn.cluster import AffinityPropagation
from sklearn.linear_model import Ridge
from sklearn.preprocessing import MinMaxScaler
from collections import Counter

"""
Global variables for: - print verbosity,
                        ... passing argument --noverbose will set it to False;
                      - randomized order of listings,
                        ... passing argument --norandom will set it to False
"""
VERBOSITY = True
RANDOMIZE_LISTINGS = True

METRO_LOCATIONS_FILE = "Amsterdam_metro_locations.txt"
PROPERTY_TYPE = "Apartment"
MAX_PRICE = 200


def printv(*args):
    """
    Prints lines if VERBOSITY == True
    """
    global VERBOSITY
    if VERBOSITY:
        for a in args:
            if a == "\n":
                print()
            else:
                print(a, end=" ")
        print()


def preprocess_data(csvfile):
    """
    Remove and adapt columns for the Airbnb data file at a given
    location.
    """
    global RANDOMIZE_LISTINGS
    global MAX_PRICE

    columns = ["host_acceptance_rate","host_response_rate",
    "host_total_listings_count","accommodates","bathrooms","bedrooms","beds",
    "amenities","price","cleaning_fee","guests_included","extra_people",
    "minimum_nights","maximum_nights","availability_30","availability_60",
    "availability_90","availability_365","number_of_reviews",
    "review_scores_rating","review_scores_accuracy","review_scores_cleanliness",
    "review_scores_checkin","review_scores_communication",
    "review_scores_location","review_scores_value",
    "calculated_host_listings_count","reviews_per_month",
    "latitude","longitude","summary","description","neighborhood_overview",
    "transit","host_response_time","neighbourhood_cleansed",
    "cancellation_policy","property_type"]

    possible_empty = ["host_total_listings_count","accommodates","bathrooms",
    "bedrooms","beds","minimum_nights","maximum_nights","availability_30",
    "availability_60","availability_90","availability_365","number_of_reviews",
    "review_scores_rating","review_scores_accuracy","review_scores_cleanliness",
    "review_scores_checkin","review_scores_communication",
    "review_scores_location","review_scores_value",
    "calculated_host_listings_count","reviews_per_month","guests_included"]

    pd.options.mode.chained_assignment = None
    data = pd.read_csv(csvfile,usecols=columns)

    # Ensure all features are converted to floats
    data = transform_percentage(data, ["host_acceptance_rate","host_response_rate"])
    data = fill_empty_entries(data, possible_empty)
    data = count_elements(data, ["amenities"])
    data = transform_host_reponse(data, "host_response_time")
    data = transform_cancellation_policy(data, "cancellation_policy")
    data = remove_dollar(data, ["price","cleaning_fee","extra_people"])

    # Add custom features "distance_to_dam" and "distance_to_metro"
    data = create_distance_to_dam(data, "latitude", "longitude")
    data = create_distance_to_metro(data, "latitude", "longitude")

    # Limit accomodations to apartments only
    N = len(data)
    data = data[data.property_type == PROPERTY_TYPE]
    printv("Pruned {} listings for having property type != {}.".format(N - len(data), PROPERTY_TYPE))
    printv("Resulting number of listings: {}.".format(len(data)), "\n")

    # Remove obsolete columns
    del data["summary"]
    del data["property_type"]
    del data["description"]
    del data["neighborhood_overview"]
    del data["transit"]
    del data["neighbourhood_cleansed"]
    del data["longitude"]
    del data["latitude"]
    del data["host_response_time"]

    # Remove outliers where listing price > MAX_PRICE
    N = len(data)
    data = data[data.price <= MAX_PRICE]
    printv("Pruned {} listings for having price > {}.".format(N - len(data), MAX_PRICE))
    printv("Resulting number of listings: {}.".format(len(data)), "\n")

    # Clip certain columns' values to an interval
    data = clip_vals(data, (0, 30), "maximum_nights")

    # Scale all columns to the interval (1,10)
    #data = scale_vals(data, (1, 10))

    if RANDOMIZE_LISTINGS:
        np.random.seed(0)
        data = data.reindex(np.random.permutation(data.index))

    return data


def scale_vals(data, interval, columns=None):
    """
    Scales values of column(s) to an interval.
    """
    scaler = MinMaxScaler(feature_range=interval)

    if not columns is None and not isinstance(columns, list):
        columns = [columns]

    if columns is None:
        # Take all columns except for 'price'
        columns = [c for c in data.columns if c not in ['price']]

    data[columns] = scaler.fit_transform(data[columns])
    return data


def clip_vals(data, interval, columns):
    """
    Clips values of column(s) to an interval.
    """
    if not isinstance(columns, list):
        columns = [columns]
    for column in columns:
        data[column] = data[column].clip(interval[0], interval[1])

    return data


def transform_percentage(data, columns):
    """
    Remove percentage signs from entries of the given
    columns of the data set.
    """
    for column in columns:
        for i, entry in enumerate(data[column]):
            if not entry or (type(entry) is not str and math.isnan(entry)):
                data[column][i] = 0
            elif type(entry) is str and "%" in entry:
                data[column][i] = int(entry[:-1])

    return data


def fill_empty_entries(data, columns):
    """
    Replaces empty entries by a zero in the given columns
    of the data set.
    """
    for column in columns:
        for i, entry in enumerate(data[column]):
            if not entry or math.isnan(entry):
                data[column][i] = 0

    return data


def count_elements(data, columns):
    """
    Replaces every entry by the number of elements
    it contains.
    """
    for column in columns:
        for i, entry in enumerate(data[column]):
            data[column][i] = len(entry.split(","))

    return data


def remove_dollar(data, columns):
    """
    Removes dollar signs from entries of the given
    columns of the data set.
    """
    for column in columns:
        for i, entry in enumerate(data[column]):
            if not entry or (type(entry) is not str and math.isnan(entry)):
                data[column][i] = 0
            elif type(entry) is str and "$" in entry:
                if "," in entry:
                    entry = entry.replace(",","")
                data[column][i] = float(entry[1:])

    return data


def transform_host_reponse(data, column):
    """
    Replaces alphabetical values for the host response column into
    numbers.
    """
    for i, entry in enumerate(data[column]):
        if (type(entry) is float and math.isnan(entry)) or entry == "a few days or more":
            data[column][i] = 4
        elif entry == "within a few hours":
            data[column][i] = 2
        elif entry == "within an hour":
            data[column][i] = 1
        elif entry == "within a day":
            data[column][i] = 3

    return data


def transform_cancellation_policy(data, column):
    """
    Replaces alphabetical values for the cancellation policy column into
    numbers.
    """
    for i, entry in enumerate(data[column]):
        if (type(entry) is float and math.isnan(entry)) or entry == "strict":
            data[column][i] = 2
        elif entry == "moderate":
            data[column][i] = 1
        elif entry == "flexible":
            data[column][i] = 0

    return data


def distance_between_locations(loc1, loc2):
    """
    Returns the distance between loc1 (lat, lon) and loc2 (lat, lon) in meters.
    SOURCE: http://stackoverflow.com/questions/4913349/haversine-formula-in-
    python-bearing-and-distance-between-two-gps-points
    """
    lon1, lat1, lon2, lat2 = map(np.radians, [loc1[1], loc1[0], loc2[1], loc2[0]])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    distance = Decimal(6367 * c)

    # Round distance to 3 decimals
    #return float(distance.quantize(Decimal('.001'), rounding=ROUND_HALF_UP))
    return distance


def create_distance_to_metro(data, Lat, Lon):
    """
    Creates new feature column with the distance to the nearest metro station
    in kilometers.
    """
    data["distance_to_metro"] = pd.Series(np.zeros(len(data)), index=data.index)
    metro_locs = []

    with open(METRO_LOCATIONS_FILE) as f:
        metro_locs = f.read().splitlines()

    for i, entry in enumerate(data[Lat]):
        distances = []
        location = (entry, data[Lon][i])

        for l in metro_locs:
            distances += [distance_between_locations(literal_eval(l)[1:], location)]

        data["distance_to_metro"][i] = min(distances)

    return data


def create_distance_to_dam(data, Lat, Lon):
    """
    Creates new feature column with the distance to the Dam of Amsterdam in
    kilometers.
    """
    dam = (52.373, 4.8932)
    data["distance_to_dam"] = pd.Series(np.zeros(len(data)), index=data.index)

    for i, entry in enumerate(data[Lat]):
        location = (entry, data[Lon][i])
        data["distance_to_dam"][i] = distance_between_locations(dam, location)

    return data


def create_boolean_keyword(data, keyword, new_col_name, case=False):
    """
    Creates new binary boolean column corresponding to the occurrence of
    'keyword' in any of the listing's strings.
    """
    data[new_col_name] = pd.Series(np.zeros(len(data), dtype=np.int), index=data.index)
    count = 0
    for i, entry in data.iterrows():
        if any(entry.str.contains(keyword, case=case, na=False, regex=False)):
            data[new_col_name][i] = 1
            count += 1

    printv("Found {} occurrences out of {} for '{}'.".format(count, len(data), keyword))
    return data


def select_features(X, y, names, nfeat):
    """
    Selects nfeat features from data, by L2 Ridge regression
    """
    result = []
    sum_coefs_selected = 0
    sum_coefs_unselected = 0

    ridge = Ridge(alpha=10)
    ridge.fit(X, y)
    printv("Selecting top {} features from Ridge feature ranking:".format(nfeat))

    zipped = zip(np.abs(ridge.coef_), names)
    lst = sorted(zipped, key = lambda x:-np.abs(x[0]))

    for i, (coef, name) in enumerate(lst):
        if i < nfeat:
            result += [name]
            sum_coefs_selected += coef
        elif i == nfeat:
            printv("Not selected:")
        else:
            sum_coefs_unselected += coef

        printv(round(coef, 3), name)

    frac_selected = sum_coefs_selected / (sum_coefs_selected + sum_coefs_unselected)
    printv("\n", "Selected features comprise {}% of Ridge regression coefficients.".format(
           round(frac_selected * 100, 2)))

    return result


def fraction_train_set_float(f):
    """
    Restricts fraction of training set to range [0.05, 0.95]
    """
    f = float(f)
    if f < 0.05 or f > 0.95:
        raise argparse.ArgumentTypeError("%r not in range [0.05, 0.95]" % (f,))

    return f


if __name__ == '__main__':

    # Define command line arguments
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@',
    )
    parser.add_argument(
        'input',
        help='Csv file with input data',
        default='listings.csv',
        nargs='?'
    )
    parser.add_argument(
        'fraction_train_set',
        help='Fraction of training set to use, between 0.05 and 0.95',
        default=0.8,
        type=fraction_train_set_float,
        nargs='?'
    )
    parser.add_argument(
        'train_x_output',
        help='Name for csv file to write output to',
        default='train_features.csv',
        nargs='?'
    )
    parser.add_argument(
        'test_x_output',
        help='Name for csv file to write output to',
        default='test_features.csv',
        nargs='?'
    )
    parser.add_argument(
        'cross_x_output',
        help='Name for csv file to write output to',
        default='cross_features.csv',
        nargs='?'
    )
    parser.add_argument(
        'train_y_output',
        help='Name for csv file to write output to',
        default='train_prices.csv',
        nargs='?'
    )
    parser.add_argument(
        'test_y_output',
        help='Name for csv file to write output to',
        default='test_prices.csv',
        nargs='?'
    )
    parser.add_argument(
        'cross_y_output',
        help='Name for csv file to write output to',
        default='cross_prices.csv',
        nargs='?'
    )
    parser.add_argument(
        '--noverbose',
        help='Disable printing verbosity',
        action='store_true'
    )
    parser.add_argument(
        '--norandom',
        help='Disable random shuffling of input rows',
        action='store_true'
    )

    # Parse arguments
    args = parser.parse_args()
    if (args.noverbose):
        VERBOSITY = False
    if (args.norandom):
        RANDOMIZE_LISTINGS = False

    # Preprocess data
    data = preprocess_data(args.input)

    # Split data into a training, test and cross-validation set
    n = int(len(data) * args.fraction_train_set)
    m = int(0.5*(len(data)-n))
    train_data = data[0:n]
    test_data = data[n:m+n]
    cross_data = data[m+n:]

    # Output the three y-vectors to CSV-file
    train_data["price"].to_csv(args.train_y_output, index=False, decimal='.')
    test_data["price"].to_csv(args.test_y_output, index=False, decimal='.')
    cross_data["price"].to_csv(args.cross_y_output, index=False, decimal='.')

    # Cluster listings by price
    X1 = data.as_matrix(columns=["price"])
    clustered = None
    try:
        # Load precomputed clusters from file
        clustered = np.load("price_clusters")
    except IOError:
        # Else: 
        clustered = AffinityPropagation(preference=-50, damping=0.94).fit(X1)

    printv("Price clusters: " + str(Counter(clustered.labels_)))

    # Remove y-vectors from datasets
    del data["price"]
    del train_data["price"]
    del test_data["price"]
    del cross_data["price"]

    # Select 10 most important features as resulting columns
    X = data.as_matrix()
    y = clustered.labels_
    names = list(data.columns.values)
    selected = select_features(X, y, names, 10)

    # Output the three X-vectors to their respective CSV-files
    train_data[selected].to_csv(args.train_x_output, decimal='.')
    test_data[selected].to_csv(args.test_x_output, decimal='.')
    cross_data[selected].to_csv(args.cross_x_output, decimal='.')
