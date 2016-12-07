# Same as learn.R only using pre-split datasets

# set this to project directory
setwd('~/fuzzybnb/')
library(frbs)
options(max.print=999999999)
features.train <- read.csv("train_features.csv", header=FALSE)
prices.train <- read.csv("train_prices.csv", header=TRUE)
features.test <- read.csv("test_features.csv", header=FALSE)
prices.test <- read.csv("test_prices.csv", header=FALSE)

# split data
data.train <- features.train
data.test <- features.test[,1:(ncol(features.test)-1)]
data.targets <- prices.test[,2]


# get range
# explanation of apply:
# https://nsaunders.wordpress.com/2010/08/20/a-brief-introduction-to-apply-in-r/
range.data <- matrix(apply(listing, 2, range), nrow=2)

# source("RLearn/learnWMmanual.R")
source("RLearn/learnWM.R")
# source("RLearn/learnHYFIS.R")
# source("RLearn/learnANFIS.R")
