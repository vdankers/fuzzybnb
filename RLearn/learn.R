# Date        : December 22, 2016
# Course      : Fundamentals of Fuzzy Logic, University of Amsterdam
# Project name: Fuzzy Bed and Breakfast
# Authors     : David Smelt, Alex Khawalid, Verna Dankers

# Description : Run prediction engine on trainingset and run test on
#       				cross validation set/test set
#               To test run learnWM/learnHYFIS/learnANFIS.R
#               To get results for parameter tweaking on cv run
#               learnWMTestParams.R or learnHYFISTestParams.R
# Usage       : Rscript learn.R or drag learn.R into R environment


# set this to project directory
setwd('~/fuzzybnb/RLearn/')
library(frbs)
options(max.print=999999999)

# read data and remove id columns
data.train <- read.csv("../Data/train_features.csv", header=TRUE)
prices <- read.csv("../Data/train_prices.csv", header=TRUE)
data.train <- cbind(data.train,prices)

data.test <- read.csv("../Data/test_features.csv", header=TRUE)
data.targets <- read.csv("../Data/test_prices.csv", header=TRUE)
data.cv <- read.csv("../Data/cross_features.csv", header=TRUE)
data.cvtargets <- read.csv("../Data/cross_prices.csv", header=TRUE)

# combine test with targets to determine range
combinedtest <- cbind(data.test,data.targets)
colnames(combinedtest)[ncol(combinedtest)] <- "price"

combinedcv <- cbind(data.cv,data.cvtargets)
colnames(combinedcv)[ncol(combinedcv)] <- "price"

# get range of inputs
range.data <- matrix(apply(rbind(data.train,combinedtest,combinedcv), 2, range), nrow=2)



# number of inputs for HYFIS and ANFIS
num_inps <- 7

source("evalMethods.R")
# source("learnWMTestParams.R")
source("learnWM.R")
# source("learnHYFIS.R")
# source("learnHYFISTestParams.R")
# source("learnANFIS.R")
