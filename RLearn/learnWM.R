# type of method
# Try out ANFIS just to see if it works
method.type <- "WM"

# a list containing all arguments
# differs per method
# 5 linguistic terms, 100 maximum iterations, step size 0.1
# tnorm is min, implication function is Zadeh, name is fuzzybnb
# implication function applies to rules, Zadeh function means
control <- list(num.labels = 5, type.mf = "GAUSSIAN", type.tnorm = "MIN",
  type.defuz = "COG", type.implication.func = "ZADEH", name = "fuzzybnbWM")

print("hoi")

# Learn rules, to get membership functions
# explanation of arguments:
# https://www.rdocumentation.org/packages/frbs/versions/3.1-0/topics/frbs.learn
object.reg <- frbs.learn(data.train, range.data, method.type, control)

# output should be [1] 5.1 4.1 4.1 2.1


# show membership functions
# pdf("WMMF.pdf")
par("mar")
par(mar=c(1,1,1,1))
plotMF(object.reg)
dev.off()

# test
res.test <- predict(object.reg, data.test)

# show error
error = sum((res.test - mean(data.targets))^2) / length(data.targets)
print(error)
