# type of method
method.type <- "HYFIS"

# a list containing all parameters
control <- list(num.labels = 5, max.iter = 100, step.size = 0.1,
  type.tnorm = "PRODUCT", type.defuz = "COG", type.implication.func = "DIENES_RESHER",
  name = "fuzzybnbHYFIS")


# Get frbs object
object.reg <- frbs.learn(data.train, range.data, method.type, control)

# show membership functions
pdf("Rplots/HYFISMF.pdf")
par("mar")
par(mar=c(1,1,1,1))
plotMF(object.reg)
dev.off()

# test
res.test <- predict(object.reg, data.test)

# show error
error = sum(abs(res.test - data.targets))/length(data.targets)
print(error)
