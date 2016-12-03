#!/usr/bin/python

"""
Date        : december 2016
Course      : Fundamentals of Fuzzy Logic, UvA
Project name: Fuzzy Bed and Breakfast
Students    : David Smelt, Alex Khawalid, Verna Dankers

Description : Preprocesses data
Usage       : python preprocessing.py input_data.csv output_prices.csv output_results.csv
"""

import argparse
import pandas
import math
import csv
import numpy as np
from math import radians, cos, sin, asin, sqrt

def preprocess_data(csvfile):
    """
    Remove and adapt columns for the Airbnb data file at a given
    location.
    """
    columns = ["host_acceptance_rate","host_response_rate",
    "host_total_listings_count","accommodates","bathrooms","bedrooms","beds",
    "amenities","price","cleaning_fee","guests_included","extra_people",
    "minimum_nights","maximum_nights","availability_30","availability_60",
    "availability_90","availability_365","number_of_reviews",
    "review_scores_rating","review_scores_accuracy","review_scores_cleanliness",
    "review_scores_checkin","review_scores_communication",
    "review_scores_location","review_scores_value","instant_bookable",
    "calculated_host_listings_count","reviews_per_month",
    "latitude","longitude","summary","description","neighborhood_overview",
    "transit","host_response_time","host_identity_verified",
    "neighbourhood_cleansed","cancellation_policy"]

    possible_empty = ["host_total_listings_count","accommodates","bathrooms",
    "bedrooms","beds","minimum_nights","maximum_nights","availability_30",
    "availability_60","availability_90","availability_365","number_of_reviews",
    "review_scores_rating","review_scores_accuracy","review_scores_cleanliness",
    "review_scores_checkin","review_scores_communication",
    "review_scores_location","review_scores_value",
    "calculated_host_listings_count","reviews_per_month","guests_included"]

    pandas.options.mode.chained_assignment = None
    data = pandas.read_csv(csvfile,usecols=columns)

    data = convert_true_false(data, ["instant_bookable","host_identity_verified"])
    data = transform_percentage(data, ["host_acceptance_rate","host_response_rate"])
    data = fill_empty_entries(data, possible_empty)
    data = count_elements(data, ["amenities"])
    data = remove_dollar(data, ["price","cleaning_fee","extra_people"])
    data = transform_host_reponse(data, "host_response_time")
    data = distance_from_locations(data, "latitude", "longitude")
    data = transform_cancellation_policy(data, "cancellation_policy")

    # Clip certain columns' values to an interval
    data = clip_vals(data, "maximum_nights", (0, 30))
    data = clip_vals(data, "distance_to_dam", (0.0, 10.0))

    # Look for occurrence of "metro" ==> new boolean column "has_metro"
    data = create_boolean_keyword(data, "metro", "has_metro")

    data = data[data.price < 1500]

    data = data.reindex(np.random.permutation(data.index))

    return data

def clip_vals(data, columns, interval):
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
    Remove dollar signs from entries of the given
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

def convert_true_false(data, columns):
    """
    Converts the 't' of true and 'f' of false into 1 and 0
    respectively, for the given columns in the data set.
    """
    for column in columns:
        for i, entry in enumerate(data[column]):
            if entry == "t":
                data[column][i] = 1
            else:
                data[column][i] = 0
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

# SOURCE: http://stackoverflow.com/questions/4913349/haversine-formula-in-
# python-bearing-and-distance-between-two-gps-points
def distance_from_locations(data, lat, lon):
    data["distance_to_dam"] = pandas.Series(np.zeros(len(data)), index=data.index)
    dam = (52.373, 4.8932)
    for i, entry in enumerate(data[lat]):
        location = (entry, data[lon][i])
        lon1, lat1, lon2, lat2 = map(radians, [location[1], location[0], dam[1], dam[0]])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        distance = 6367 * c

        # round distance to 3 decimals with Python2 string formatting
        # data["distance_to_dam"][i] = "{:10.3f}".format(round(distance, 3))
        data["distance_to_dam"][i] = distance
        #print distance, "->", data["distance_to_dam"][i]
    return data

def create_boolean_keyword(data, keyword, new_col_name, case=False):
    """
    Creates new binary boolean column corresponding to the occurrence of
    'keyword' in any of the listing's strings.
    """
    data[new_col_name] = pandas.Series(np.zeros(len(data), dtype=np.int), index=data.index)
    count = 0
    for i, entry in data.iterrows():
        if any(entry.str.contains(keyword, case=case, na=False, regex=False)):
            data[new_col_name][i] = 1
            count += 1

    print "Found {0} occurrences out of {1} for '{2}'.".format(count, len(data), keyword)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@',
    )

    parser.add_argument(
        'input',
        help="Csv file with input data",
        default='setje.csv', # first 1000 listings
        nargs='?'
    )

    parser.add_argument(
        'x_output',
        help="Name for csv file to write output to",
        default='result.csv',
        nargs='?'
    )

    parser.add_argument(
        'y_output',
        help="Name for csv file to write output to",
        default='prices.csv',
        nargs='?'
    )

    args = parser.parse_args()

    data = preprocess_data(args.input)

    prices = data["price"].to_csv(args.y_output)

    del data["summary"]
    del data["description"]
    del data["neighborhood_overview"]
    del data["transit"]
    del data["neighbourhood_cleansed"]
    del data["longitude"]
    del data["latitude"]
    del data["price"]

    data = data.to_csv(args.x_output)

