# Date        : december 2016
# Course      : Fundamentals of Fuzzy Logic, University of Amsterdam
# Project name: Fuzzy Bed and Breakfast
# Authors     : David Smelt, Alex Khawalid, Verna Dankers

# Description : Run prediction engine on trainingset and run test on
#				cross validation set/test set
# Usage       : Rscript learn.R


# set this to project directory
setwd('~/fuzzybnb/RLearn/')
library(frbs)
options(max.print=999999999)

# read data and remove id columns
data.train <- read.csv("../train_features.csv", header=TRUE)
prices <- read.csv("../train_prices.csv", header=FALSE)
prices <- prices[,1]
data.train <- cbind(data.train[,2:ncol(data.train)],prices)

data.test <- read.csv("../test_features.csv", header=TRUE)
data.test <- data.test[, 2:ncol(data.test)]
data.targets <- read.csv("../test_prices.csv", header=FALSE)
data.targets <- data.targets[,1]

# combine test with targets to determine range
combinedtest <- cbind(data.test,data.targets)
colnames(combinedtest)[ncol(combinedtest)] <- "prices"

range.data <- matrix(apply(rbind(data.train,combinedtest), 2, range), nrow=2)

# split test into cv and test
data.cv <- data.test[1:(0.5*nrow(data.test)),]
data.cvtargets <- data.targets[1:(0.5*length(data.targets))]

data.test <- data.test[(0.5*nrow(data.test)):nrow(data.test),]
data.targets <- data.targets[(0.5*length(data.targets)):length(data.targets)]

# number of inputs for HYFIS and ANFIS
num_inps <- 4

# get range of inputs

# source("learnWMTestParams.R")
# source("learnWM.R")
# source("learnHYFIS.R")
source("learnHYFISTestParams.R")
# source("learnANFIS.R")
