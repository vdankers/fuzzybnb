# type of method
method.type <- "HYFIS"


# reduce inputs for HYFIS and ANFIS
data.train <- cbind(data.train[,1:num_inps],prices)
data.test <- data.test[,1:num_inps]
data.cv <- data.cv[,1:num_inps]


# a list with all parameters
control <- list(num.labels = 6, max.iter = 100, step.size = 0.1,
  type.tnorm = "PRODUCT", type.defuz = "COG", type.implication.func = "DIENES_RESHER",
  name = "fuzzybnbHYFIS")


object.reg <- frbs.learn(data.train, cbind(range.data[,1:num_inps],range.data[,ncol(range.data)]), method.type, control)

# show membership functions
pdf("Rplots/HYFISMF.pdf")
par("mar")
par(mar=c(1,1,1,1))
plotMF(object.reg)
dev.off()

# test
res.test <- predict(object.reg, data.test)

# show error
error = sum(abs(res.test - data.test))/length(data.test)
print(error)
sum((res.test-data.targets)/data.targets)/length(data.targets)

save.image(file="HYFIS")
