# Run in terminal with:
# Rscript learn.R
# set working directory to script location
# werkt nog niet echt
# this.dir <- dirname(parent.frame(2)$ofile)

# split into train, test and cv. Remaining data is for cv
split.train <- 0.6
split.test <- 0.2 + split.train

# set this to project directory
setwd("/Users/alexkhawalid/fuzzybnb")
library(frbs)
options(max.print=999999999)
listing = read.csv("result.csv", header= TRUE)
prices = read.csv("prices.csv", header=TRUE)


# split data
data.train <- listing[1 : (split.train*nrow(listing)),1:3]
data.test <- listing[(split.train*nrow(listing)) : split.test*nrow(listing), 1:3]
data.cv <- listing[(split.test*nrow(listing)) : nrow(listing), 1:3]
data.targets <- prices[0:split.train*nrow(prices), 1]

print("Number of columns in data for train, test and cross validation respectively")
print(ncol(data.train))
print(ncol(data.test))
print(ncol(data.cv))

# get range
# explanation of apply:
# https://nsaunders.wordpress.com/2010/08/20/a-brief-introduction-to-apply-in-r/
range.data <-apply(data.train, 2, range)

# type of method
# Try out ANFIS just to see if it works
method.type <- "WM"

# a list containing all arguments
# differs per method
# 5 linguistic terms, 100 maximum iterations, step size 0.1
# tnorm is min, implication function is Zadeh, name is fuzzybnb
# implication function applies to rules, Zadeh function means
control <- list(num.labels = 5, type.mf = "GAUSSIAN", type.tnorm = "MIN"
  type.defuz = "COG", type.implication.func = "ZADEH", name = "fuzzybnbWM")

print("hoi")

# Learn rules, to get membership functions
# explanation of arguments:
# https://www.rdocumentation.org/packages/frbs/versions/3.1-0/topics/frbs.learn
object.reg <- frbs.learn(data.train, range.data, method.type, control)

# output should be [1] 5.1 4.1 4.1 2.1
par("mar")

par(mar=c(1,1,1,1))

# show membership functions
plotMF(object.reg)

# test
res.test <- predict(object.reg, data.test)

# show error
error = sum((res.test - mean(data.targets))^2) / length(data.targets)
print(error)
