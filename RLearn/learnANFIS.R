# type of method
method.type <- "ANFIS"

# List of parameters for the prediction engine
control <- list(num.labels = 5, max.iter = 100, step.size = 0.1,
  type.tnorm = "PRODUCT", type.implication.func = "DIENES_RESHER", name = "fuzzybnbANFIS")

# Get frbs object
object.reg <- frbs.learn(data.train, range.data, method.type, control)

# show membership functions
pdf("RLearn/ANFISMF.pdf")
par("mar")

par(mar=c(1,1,1,1))
plotMF(object.reg)
dev.off()

# test
res.test <- predict(object.reg, data.test)

# show error
error = sum(abs(res.test - data.targets))/length(data.targets)
print(error)
