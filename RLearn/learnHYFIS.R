# type of method
method.type <- "HYFIS"


# reduce inputs for HYFIS and ANFIS
data.train <- cbind(data.train[,1:num_inps],prices)
data.test <- data.test[,1:num_inps]



# a list with all parameters
control <- list(num.labels = 5, max.iter = 100, step.size = 0.1,
  type.tnorm = "PRODUCT", type.defuz = "COG", type.implication.func = "DIENES_RESHER",
  name = "fuzzybnbHYFIS")


object.reg <- frbs.learn(data.train, range.data[,1:num_inps], method.type, control)

# show membership functions
pdf("Rplots/HYFISMF.pdf")
par("mar")
par(mar=c(1,1,1,1))
plotMF(object.reg)
dev.off()

# test
res.cv <- predict(object.reg, data.cv)

# show error
error = sum(abs(res.cv - data.cvtargets))/length(data.cvtargets)
print(error)

save.image(file="HYFIS")
