methods <- list("WM","HYFIS","ANFIS")

# split into train, test and cv. Remaining data is for cv
split.train <- 0.6
split.test <- 0.2 + split.train

# set this to project directory
setwd('C:\\Users\\Alex\\Documents\\GitHub\\fuzzybnb')
library(frbs)
options(max.print=999999999)
listing <- read.csv("result_trim.csv", header= TRUE)
prices <- read.csv("prices_trim.csv", header=TRUE)

listing <- cbind(listing,prices[0:nrow(prices),2])

listing <- norm.data(listing, apply(listing, 2, range), min.scale = 0, max.scale = 1 )
prices <- norm.data(prices, apply(prices, 2, range), min.scale = 0, max.scale = 1 )



# split data
data.train <- listing[1 : (split.train*nrow(listing)),1:ncol(listing)]
data.test <- listing[(split.train*nrow(listing)) : (split.test*nrow(listing)), 1:(ncol(listing)-1)]
data.cv <- listing[(split.test*nrow(listing)) : nrow(listing), 1:ncol(listing)]
data.targets <- prices[(split.train*nrow(prices)) : (split.test*nrow(prices)), 2]


# get range
# explanation of apply:
# https://nsaunders.wordpress.com/2010/08/20/a-brief-introduction-to-apply-in-r/
range.data <- matrix(apply(listing, 2, range), nrow=2)

source("RLearn/learnWM.R")
source("RLearn/learnHYFIS.R")
source("RLearn/learnANFIS.R")
