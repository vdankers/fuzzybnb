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
listing = read.csv("output.csv", header= TRUE)

# split data
data.train <- listing[1 : (split.train*nrow(listing)),0:(ncol(listing))]
data.test <- listing[(split.train*nrow(listing)) : split.test*nrow(listing), 0: (ncol(listing))]
data.cv <- listing[(split.test*nrow(listing)) : nrow(listing), 0: (ncol(listing))]
data.targets <- listing[(split.train*nrow(listing)): nrow(listing),ncol(listing)]

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
method.type <- "ANFIS"

# a list containing all arguments
# differs per method
# 5 linguistic terms, 100 maximum iterations, step size 0.1
# tnorm is min, implication function is Zadeh, name is fuzzybnb
# implication function applies to rules, Zadeh function means
######################################################
# IF a < 0.5 OR 1 - a < b THEN
#  IF TRUE
#    return 1 - a
#  ELSE
#    IF a < b THEN
#      IF TRUE
#        return a
#      ELSE
#        return b
# (a < 0.5 || 1 - a > b ? 1 - a : (a < b ? a : b))
######################################################
control <- list(num.labels = 5, max.iter = 100, step.size = 0.1,
  type.tnorm = "MIN", type.implication.func = "ZADEH", name = "fuzzybnb")


# Learn rules, to get membership functions
# explanation of arguments:
# https://www.rdocumentation.org/packages/frbs/versions/3.1-0/topics/frbs.learn
object.reg <- frbs.learn(data.train, range.data, method.type, control)

# show membership functions
plotMF(object.reg)
