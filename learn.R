# Read data and apply FLS

# split into train, test and cv. Remaining data is for cv
split.train <- 0.6
split.test <- 0.2 + split.train

# set this to project directory
setwd('~/fuzzybnb/')
library(frbs)
options(max.print=999999999)
listing <- read.csv("result.csv", header=TRUE)
prices <- read.csv("prices.csv", header=FALSE)


# Remove id columns
listing <- cbind(listing[1:(nrow(listing)),2:ncol(listing)],prices[,2])

# split data
data.train <- listing[1 : (split.train*nrow(listing)),]
data.test <- listing[(split.train*nrow(listing)) : (split.test*nrow(listing)), 1:(ncol(listing)-1)]
data.cv <- listing[(split.test*nrow(listing)) : nrow(listing), 1:ncol(listing)]
data.targets <- prices[(split.train*nrow(prices)) : (split.test*nrow(prices)), 2]


write.csv(data.train[,1:(ncol(data.train)-1)], file ="train_features_r.csv")
write.csv(data.train[,ncol(data.train)], file ="train_prices_r.csv")
write.csv(data.cv[,1:(ncol(data.cv)-1)], file ="cv_features_r.csv")
write.csv(data.cv[,ncol(data.cv)], file ="cv_prices_r.csv")
write.csv(data.test, file ="test_features_r.csv")
write.csv(data.targets, file ="test_prices.csv")

# get range of inputs
# explanation of apply:
# https://nsaunders.wordpress.com/2010/08/20/a-brief-introduction-to-apply-in-r/
range.data <- matrix(apply(listing, 2, range), nrow=2)

source("RLearn/learnWMTestParams.R")
# source("RLearn/learnWMmanual.R")
source("RLearn/learnWM.R")
# source("RLearn/learnHYFIS.R")
# source("RLearn/learnANFIS.R")
