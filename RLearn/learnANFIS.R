# type of method
method.type <- "ANFIS"


# a list containing parameters frbs.learn
control <- list(num.labels = 5, max.iter = 100, step.size = 0.1,
  type.tnorm = "PRODUCT", type.implication.func = "DIENES_RESHER", name = "fuzzybnbANFIS")

# Make frbs object
object.reg <- frbs.learn(data.train, range.data, method.type, control)

# show membership functions
pdf("Rplots/ANFISMF.pdf")
par("mar")
par(mar=c(1,1,1,1))
plotMF(object.reg)
dev.off()

# test
res.cv <- predict(object.reg, data.test)

# show error
error = sum(abs(res.cv - data.targets))/length(data.targets)
print(error)

save.image(file="/RWorkspaces/ANFIS")
