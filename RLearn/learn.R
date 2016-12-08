# Date        : december 2016
# Course      : Fundamentals of Fuzzy Logic, University of Amsterdam
# Project name: Fuzzy Bed and Breakfast
# Authors     : David Smelt, Alex Khawalid, Verna Dankers

# Description : Run prediction engine on trainingset and run test on
#				cross validation set/test set
# Usage       : Rscript learn.R


# set this to project directory
# setwd('~/fuzzybnb/RLearn/')
library(frbs)
options(max.print=999999999)

# read data and remove id columns
data.train <- read.csv("../train_features.csv", header=TRUE)
prices <- read.csv("../train_prices.csv", header=FALSE)
data.train <- cbind(data.train[,2:ncol(data.train)],prices)

data.test <- read.csv("../test_features.csv", header=TRUE)
data.test <- data.test[, 2:ncol(data.test)]
data.targets <- read.csv("../train_prices.csv", header=FALSE)

# get range of inputs
range.data <- matrix(apply(rbind(data.train,cbind(data.test,data.targets)), 2, range), nrow=2)

# source("learnWMTestParams.R")
source("learnWM.R")
# source("learnHYFIS.R")
# source("learnANFIS.R")
