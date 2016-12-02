methods <- list("WM","HYFIS","ANFIS")

# split into train, test and cv. Remaining data is for cv
split.train <- 0.6
split.test <- 0.2 + split.train

# set this to project directory
setwd("/Users/alexkhawalid/fuzzybnb")
library(frbs)
options(max.print=999999999)
listing = read.csv("result_trim.csv", header= TRUE)
prices = read.csv("prices_trim.csv", header=TRUE)


# split data
data.train <- listing[1 : (split.train*nrow(listing)),1:ncol(listing)]
data.test <- listing[(split.train*nrow(listing)) : split.test*nrow(listing), 1:ncol(listing)]
data.cv <- listing[(split.test*nrow(listing)) : nrow(listing), 1:ncol(listing)]
data.targets <- prices[0:split.train*nrow(prices), 1]

print("Number of columns in data for train, test and cross validation respectively")
print(ncol(data.train))
print(ncol(data.test))
print(ncol(data.cv))

# get range
# explanation of apply:
# https://nsaunders.wordpress.com/2010/08/20/a-brief-introduction-to-apply-in-r/
range.data <-apply(data.train, 2, range)

# source("RLearn/learnWM.R")
source("RLearn/learnHYFIS.R")
# source("RLearn/learnANFIS.R")
